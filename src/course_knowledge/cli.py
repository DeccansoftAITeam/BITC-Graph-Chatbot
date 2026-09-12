"""Developer commands for the teaching platform."""

from __future__ import annotations

import argparse
from pathlib import Path

from .content import child_chunks, markdown_sections
from .database import KnowledgeWriter, apply_migrations, connect
from .ingestion import build_ingestion_plan
from .graph import GraphProjector
from .embeddings import AzureOpenAIEmbedder
from .database import pending_chunks, store_embeddings
from .settings import azure_openai_settings, content_safety_settings
from .hybrid import HybridRetriever
from .graph_retrieval import GraphExpander
from .answers import GroundedAnswerer
from .evaluation import load_questions, source_hit, summarize
from .safety import ContentSafetyGate
from .inventory import build_inventory, inventory_report
from .settings import database_settings
from .settings import blob_storage_settings
from .storage import BlobAssetStore


def validate_content(project_root: Path) -> None:
    _, placements = build_inventory(project_root)
    markdown = [item for item in placements if item.source_type == "markdown"]
    section_count = 0
    chunk_count = 0
    for item in markdown:
        text = (project_root / item.source_path).read_text(encoding="utf-8")
        sections = markdown_sections(text)
        section_count += len(sections)
        chunk_count += sum(len(child_chunks(section)) for section in sections)
    print(f"Validated {len(markdown)} Markdown sources: {section_count} parent sections, {chunk_count} child chunks")


def main() -> None:
    parser = argparse.ArgumentParser(prog="course-knowledge")
    parser.add_argument("--project-root", type=Path, default=Path.cwd())
    commands = parser.add_subparsers(dest="command", required=True)
    inventory = commands.add_parser("inventory", help="write a content-addressed source inventory")
    inventory.add_argument("--output", type=Path, default=Path("var/source-inventory.json"))
    commands.add_parser("validate-content", help="validate Markdown parent-child extraction")
    commands.add_parser("migrate", help="apply PostgreSQL schema migrations")
    ingest = commands.add_parser("ingest", help="ingest catalog and supplied source content into PostgreSQL")
    ingest.add_argument("--course-id", help="ingest one course, allowing resumable bulk loads")
    commands.add_parser("sync-graph", help="project verified course structure to Apache AGE")
    commands.add_parser("upload-assets", help="upload the supplied source assets to Azure Blob Storage and update source URIs")
    embed = commands.add_parser("embed", help="generate and store Azure OpenAI embeddings")
    embed.add_argument("--batch-size", type=int, default=32)
    search = commands.add_parser("search", help="run hybrid keyword and vector retrieval")
    search.add_argument("query")
    search.add_argument("--limit", type=int, default=5)
    search.add_argument("--graph", action="store_true", help="attach bounded AGE graph context")
    compare = commands.add_parser("compare", help="compare baseline retrieval with GraphRAG context expansion")
    compare.add_argument("query")
    compare.add_argument("--limit", type=int, default=3)
    ask = commands.add_parser("ask", help="generate a grounded answer with AGE context and citations")
    ask.add_argument("question")
    ask.add_argument("--limit", type=int, default=5)
    ask.add_argument("--moderate", action="store_true", help="moderate question and answer with Azure AI Content Safety")
    evaluate = commands.add_parser("evaluate", help="score retrieval against anonymized golden questions")
    evaluate.add_argument("--file", type=Path, default=Path("evals/golden-questions.json"))
    evaluate.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    root = args.project_root.resolve()
    if args.command == "inventory":
        courses, placements = build_inventory(root)
        output = args.output if args.output.is_absolute() else root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        import json
        output.write_text(json.dumps(inventory_report(courses, placements), indent=2) + "\n", encoding="utf-8")
        print(f"Inventory written to {output}")
    elif args.command == "validate-content":
        validate_content(root)
    elif args.command == "migrate":
        with connect(database_settings()) as connection:
            apply_migrations(connection, root / "migrations")
    elif args.command == "ingest":
        plan = build_ingestion_plan(root)
        if args.course_id:
            plan = plan.for_course(args.course_id)
        with connect(database_settings()) as connection:
            summary = KnowledgeWriter(connection).ingest(plan)
        print("Ingested " + ", ".join(f"{key}={value}" for key, value in summary.items()))
    elif args.command == "sync-graph":
        with connect(database_settings()) as connection:
            summary = GraphProjector(connection).sync()
        print("Graph synchronized " + ", ".join(f"{key}={value}" for key, value in summary.items()))
    elif args.command == "upload-assets":
        plan = build_ingestion_plan(root)
        store = BlobAssetStore(blob_storage_settings())
        uploaded = 0
        with connect(database_settings()) as connection, connection.cursor() as cursor:
            for prepared in plan.sources:
                item = prepared.placement
                content = (root / item.source_path).read_bytes()
                uri = store.upload(f"courses/{item.course_id}/{item.module_key}/{item.content_sha256}-{Path(item.source_path).name}", content)
                cursor.execute("UPDATE sources SET storage_uri=%s WHERE content_sha256=%s", (uri, item.content_sha256))
                uploaded += 1
            connection.commit()
        print(f"Blob asset upload complete: {uploaded} course file placements")
    elif args.command == "embed":
        azure = azure_openai_settings()
        embedder = AzureOpenAIEmbedder.from_settings(azure)
        total = 0
        with connect(database_settings()) as connection:
            while chunks := pending_chunks(connection, azure.embedding_deployment, args.batch_size):
                store_embeddings(connection, chunks, embedder.embed([chunk["text_content"] for chunk in chunks]), azure.embedding_deployment)
                total += len(chunks)
                print(f"Embedded {total} chunks")
        print(f"Embedding complete: {total} chunks with {azure.embedding_deployment}")
    elif args.command == "evaluate":
        questions_file = args.file if args.file.is_absolute() else root / args.file
        questions = load_questions(questions_file)
        azure = azure_openai_settings()
        hits: list[bool] = []
        with connect(database_settings()) as connection:
            retriever = HybridRetriever(connection, AzureOpenAIEmbedder.from_settings(azure))
            for question in questions:
                hit = source_hit(retriever.search(question.question, args.limit), question.expected_sources)
                hits.append(hit)
                print(f"{question.question_id}: {'HIT' if hit else 'MISS'}")
        print(summarize(hits))
    elif args.command in {"search", "compare", "ask"}:
        azure = azure_openai_settings()
        with connect(database_settings()) as connection:
            query = args.question if args.command == "ask" else args.query
            results = HybridRetriever(connection, AzureOpenAIEmbedder.from_settings(azure)).search(query, args.limit)
            expander = GraphExpander(connection) if args.command in {"compare", "ask"} or getattr(args, "graph", False) else None
            if args.command == "ask":
                safety = ContentSafetyGate.from_settings(content_safety_settings()) if args.moderate else None
                if safety and not safety.assess(query).allowed:
                    print("Question blocked by Content Safety")
                    return
                contexts = {result.candidate.metadata["source_id"]: expander.from_source(result.candidate.metadata["source_id"]) for result in results}
                answer = GroundedAnswerer(azure).answer(query, results, contexts)
                if safety and not safety.assess(answer.text).allowed:
                    print("Generated answer blocked by Content Safety")
                    return
                print(answer.text)
                print("\nCITATIONS:")
                for index, citation in enumerate(answer.citations, start=1):
                    print(f"[{index}] {citation}")
                return
            if args.command == "compare":
                print("BASELINE: keyword + vector + RRF")
        for index, result in enumerate(results, start=1):
            metadata = result.candidate.metadata
            print(f"{index}. [{', '.join(result.matched_legs)}] {metadata['course_title']} / {metadata['module_title']} / {metadata['source']}")
            print("   " + result.candidate.text.replace("\n", " ")[:220])
            if expander:
                with connect(database_settings()) as graph_connection:
                    context = GraphExpander(graph_connection).from_source(metadata["source_id"])
                if context:
                    print("   GRAPH: " + " | ".join(f"{item.course} -> {item.module} -> {item.technology}" for item in context))
        if args.command == "compare":
            print("GRAPHRAG: same evidence chunks plus the AGE paths marked GRAPH above")
    else:
        azure = azure_openai_settings()
        embedder = AzureOpenAIEmbedder.from_settings(azure)
        total = 0
        with connect(database_settings()) as connection:
            while chunks := pending_chunks(connection, azure.embedding_deployment, args.batch_size):
                store_embeddings(connection, chunks, embedder.embed([chunk["text_content"] for chunk in chunks]), azure.embedding_deployment)
                total += len(chunks)
                print(f"Embedded {total} chunks")
        print(f"Embedding complete: {total} chunks with {azure.embedding_deployment}")
