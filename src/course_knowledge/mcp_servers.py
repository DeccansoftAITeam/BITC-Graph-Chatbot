"""Separate, least-privilege MCP profiles over the course knowledge service."""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .services import CourseKnowledgeService


def create_author_server(service: CourseKnowledgeService | None = None) -> FastMCP:
    """Author/instructor tools: read-only catalogue, retrieval, and graph context."""
    knowledge = service or CourseKnowledgeService()
    mcp = FastMCP(
        "BestITCourses Authoring Knowledge",
        instructions=(
            "Use this BestITCourses.com MCP server only for authorized instructors and course authors. "
            "It searches BestITCourses training material about GitHub Copilot, Azure OpenAI, RAG, MCP, "
            "and related developer topics. Use search_knowledge for factual course questions; use "
            "list_courses, list_modules, and get_module_content for curriculum navigation. Results are "
            "read-only. Never claim that graph context is lesson evidence."
        ),
        website_url="https://bestitcourses.com",
    )

    @mcp.tool(name="bestitcourses_list_courses", title="Browse BestITCourses author catalogue")
    def list_courses() -> list[dict]:
        """Use when an instructor asks which BestITCourses courses exist; do not use for lesson answers."""
        return knowledge.list_courses()

    @mcp.tool(name="bestitcourses_list_modules", title="Browse a BestITCourses course curriculum")
    def list_modules(course_key: str) -> list[dict]:
        """Use after selecting a BestITCourses course to navigate its latest module sequence."""
        return knowledge.list_modules(course_key)

    @mcp.tool(name="bestitcourses_get_module_assets", title="Get instructor module source metadata")
    def get_module_content(course_key: str, module_key: str) -> list[dict]:
        """Use only when an instructor needs BestITCourses source-asset metadata for a selected module."""
        return knowledge.module_content(course_key, module_key)

    @mcp.tool(name="bestitcourses_search_author_knowledge", title="Search BestITCourses teaching knowledge")
    def search_knowledge(query: str, limit: int = 5, include_graph_context: bool = True) -> list[dict]:
        """Use for an instructor's factual question about BestITCourses course content. Returns cited excerpts and optional bounded curriculum graph context."""
        return knowledge.search(query, limit, graph_context=include_graph_context)

    return mcp


def create_student_server(service: CourseKnowledgeService | None = None) -> FastMCP:
    """Student tools: course-scoped learning and cited answers, with no author surface."""
    knowledge = service or CourseKnowledgeService()
    mcp = FastMCP(
        "BestITCourses Student Learning",
        instructions=(
            "This is the BestITCourses.com student learning MCP server. Use it only when a learner asks "
            "about BestITCourses course material, lessons, GitHub Copilot, Azure OpenAI, RAG, MCP, or "
            "other topics covered by their BestITCourses course. First use bestitcourses_student_search "
            "to locate cited learning material; use bestitcourses_student_ask for a concise grounded answer. "
            "Do not use this server for unrelated general knowledge. Treat returned citations as the source "
            "of truth and say when course material does not support an answer."
        ),
        website_url="https://bestitcourses.com",
    )

    @mcp.tool(name="bestitcourses_student_courses", title="Browse BestITCourses learning courses")
    def list_learning_courses() -> list[dict]:
        """Use when a learner asks which BestITCourses courses they can study. Remote deployment applies enrolment policy."""
        return knowledge.list_courses()

    @mcp.tool(name="bestitcourses_student_modules", title="Browse BestITCourses lesson modules")
    def list_course_modules(course_key: str) -> list[dict]:
        """Use to help a learner navigate lessons in one selected BestITCourses course."""
        return knowledge.list_modules(course_key)

    @mcp.tool(name="bestitcourses_student_search", title="Search BestITCourses course material")
    def search_learning(course_key: str, query: str, limit: int = 5) -> list[dict]:
        """Use before answering a learner's BestITCourses question when cited excerpts will help. Searches only the specified course."""
        return knowledge.search(query, limit, course_key=course_key, graph_context=False)

    @mcp.tool(name="bestitcourses_student_ask", title="Answer from BestITCourses course material")
    def ask_course(course_key: str, question: str, limit: int = 5) -> dict:
        """Use for a learner's question about one BestITCourses course. Produces a grounded, cited answer; Azure Content Safety is always applied."""
        return knowledge.ask(question, course_key, limit, moderate=True)

    return mcp


def run_author() -> None:
    create_author_server().run(transport="stdio")


def run_student() -> None:
    create_student_server().run(transport="stdio")
