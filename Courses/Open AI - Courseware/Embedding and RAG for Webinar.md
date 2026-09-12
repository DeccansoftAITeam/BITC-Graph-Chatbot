**Understanding Embeddings**

**What is a Token?**

* A building block of text. It’s a unit of text that the model processes.
* Tokens can be:
  + Words
  + Subwords
  + Characters
  + Punctuation
* LLMs don’t process raw text — they work on tokens.

![A number of colored text  AI-generated content may be incorrect.](data:image/png;base64...)

**What is Vector?**

Vectors are **multi-valued numeric representations** of information, for example [10, 3, 1] in which each numeric element represents a particular attribute of the information. Each dimension of the vector represents some aspect or attribute of the data.

Imagine a **pet’s dataset** where each pet is represented by three attributes:

* **Size** (on a scale from 1 to 10, where 1 is very small and 10 is very large).
* **Friendliness** (on a scale from 1 to 10, where 1 is not friendly and 10 is very friendly).
* **Energy Level** (on a scale from 1 to 10, where 1 is very low energy and 10 is very high energy).

|  |  |
| --- | --- |
| **Examples: Pet Animals**  **Dog**: [6, 9, 8]  **Cat**: [4, 7, 5]  **Hamster**: [1, 6, 7]  **Rabbit**: [3, 8, 6]  **Parrot**: [2, 7, 9] | ![Output image](data:image/png;base64...) |

**Observations:** Pets with similar attributes will have vectors that are close together.

* **cat** and **rabbit** are relatively close because their size, friendliness, and energy levels are similar.
* **dog** and **hamster** are far apart in vector space, since the dog is larger and has a different energy level.
* If you wanted to find a pet that’s **friendly and has high energy**, **dog** and **parrot** would stand.
* If someone wanted a **low-energy** pet, **cat** or **rabbit** might be better choices.

**What are [Vector] Embeddings**

* In Large Language Models (LLMs), embeddings are numerical representations of text, like words, phrases, or entire documents, that capture semantic meaning (context of words and phrases, allowing LLMs to understand how their meaning changes depending on the surrounding text).
* Imagine an *n*-dimensional space with thousands of attributes about any **word's grammar, meaning, and use in sentences** mapped to a series of numbers. It retains the **contextual significance of data.**
* The key feature of embeddings is that **similar items** will have vectors that are **close together** in this vector space, even if the original data is very different.

**For example:**

* "king" and "queen" are **semantically related** → so their embeddings will be **close in vector space**

|  |  |
| --- | --- |
| ![Word Embedding: Basics. Create a vector from a word | by Hariom Gautam |  Medium](data:image/png;base64...) | ![A diagram of different colored dots  Description automatically generated](data:image/png;base64...) |

These embeddings are learned and abstracted from the data, and their dimensions **don't correspond to any specific attributes** like size, friendliness, or energy.

**Embeddings are commonly used for:**

* **Search** (where results are ranked by relevance to a query string)
  + Finding similar documents, matching questions to answers, duplicate detection.
  + **Use Case**: Search engines, recommendation systems, chatbot intent matching.
* **Clustering** (where text strings are grouped by similarity)
  + Group similar text embeddings into clusters.
  + **Use Case**: Organizing articles, grouping customer feedback, topic modeling.
* **Classification** (where text strings are classified by their most similar label)
  + Classify text into predefined categories.
  + **Use Case**: Spam detection, sentiment analysis, document categorization
* **Anomaly detection** (where outliers with little relatedness are identified)
  + Identify outliers in a dataset by computing distances from a cluster center.
  + **Use Case**: Fraud detection, unusual behavior detection.
* **Recommendations (where items with related text strings are recommended)**
* Recommend content that is semantically similar to user preferences or input.
* **Use Cases:** Personalized content feeds, Product recommendations, Course or video suggestions

**What is Cosine Similarity**?

Measures the cosine of the angle between two vectors, useful for determining how similar two embeddings are. Ranges from -1 to 1.

How to Interpret Cosine Similarity Scores

* **1.0** → The strings are identical
* **0.8 - 0.99** → Very similar meaning
* **0.5 - 0.79** → Somewhat similar
* **0.2 - 0.49** → Weak similarity
* **0.0 - 0.19** → Very different

**Embedding Models**

OpenAI offers two powerful third-generation embedding model (denoted by -3 in the model ID).

* **text-embedding-3-small**
* **text-embedding-3-large**

**Example: Single Input Text**

**Install Package**

pip install numpy

**demo.py**

from openai import OpenAI

import os

import numpy as np

client = OpenAI()

sentences = [

    "This is a Sample Code of OpenAI",

    "OpenAI Sample Code:",

    "Today is a holiday"

]

response = **client.embeddings.create**(

  input= sentences,

  model="text-embedding-3-large",

)

print(response.data[0].embedding)

print(response.data[1].embedding)

# Calculate Cosine Similariy

def **cosine\_similarity**(a, b):

    return np.dot(a, b) / (np.linalg.norm(a) \* np.linalg.norm(b))

print("Cosine Similarity:", cosine\_similarity(response.data[0].embedding, response.data[1].embedding))

print("Cosine Similarity:", cosine\_similarity(response.data[0].embedding, response.data[2].embedding))

**Note: In the above example,** response.data is having only one element because input is only one string.

**Embedding Response**

{

"object": "list",

"**data**": [

{

"object": "embedding",

"index": 0,

"**embedding**": [

-0.006929283495992422,

-0.005336422007530928,

... (omitted for spacing)

-4.547132266452536e-05,

-0.024047505110502243

],

}

],

"model": "text-embedding-3-small",

"usage": {

"prompt\_tokens": 5,

"total\_tokens": 5

}

}

**About Vector Database**

* A **vector database** is a type of database systems designed to efficiently **store, index, and query** data in the form of vectors.
* **Indexing** employs advanced data structures such as **FAISS (Facebook AI Similarity Search)**, **HNSW (Hierarchical Navigable Small World graphs)**, or **LSH (Locality Sensitive Hashing)** for efficient querying in high-dimensional spaces.
* **Scalability:** Designed to handle millions or billions of vectors while maintaining fast query times.

![A diagram of different types of embedding  AI-generated content may be incorrect.](data:image/png;base64...)

**Popular Vector Databases:**

1. **OpenSearch with KNN Plugin**
2. **PostgreSQL (with pgvector plugin)**
3. **Mysql (**MySQL HeatWave ML)
4. **Pinecone:** Specialized for machine learning use cases with fast and scalable similarity search.
5. **Weaviate:** Offers semantic search and supports various ML models.
6. **Chroma:** Focused on AI-first applications with seamless ML integration.
7. **Vespa:** Handles both structured and unstructured data queries.
8. **.** . .

**Retrieval-Augmented Generation (RAG)**

In the landscape of conversational AI, Large Language Models (LLMs) are akin to encyclopedic repositories of general knowledge. They have an extensive **breadth** of information but often **lack depth** in specific, localized contexts, such as the intricacies of a company’s internal database or the specialized findings of a research paper.

**![A screenshot of a phone  Description automatically generated](data:image/png;base64...)**

* RAG uses your data to generate answers to the user question.
* It allows your LLM to have domain-specific external information sources like your databases, documents, etc in real time. This way the LLM can get the most up-to-date and relevant information to answer the queries specific to your business.
* RAG has shown promising results in improving the accuracy and relevance of generated responses, especially in scenarios where the answer requires synthesizing information from multiple sources. It leverages the strengths of both information retrieval and language generation to provide better answers.

In **RAG (Retrieval-Augmented Generation)**, the term **RAG** stands for:

1. **Retrieval**: This refers to fetching relevant documents or pieces of information from an external knowledge source (such as a vector database, knowledge base, or internet search) based on the user's query.
2. **Augmentation**: The retrieved documents are then used to **enhance** the generative model’s response. Instead of relying only on the pre-trained knowledge, the model gets **real-time** context from the retrieved data.
3. **Generation**: The augmented data is passed to a language model (like GPT-4) to **generate** a final, more accurate, and informed response based on both its training data and the retrieved documents.

**Prompt : “What is the price of Microsoft Stock today?” or “What is the temperature in London today”**

**@** <https://chatgpt.com/>

**Here’s a high-level overview of how a RAG system works:**

**![A diagram of a chatbot  Description automatically generated](data:image/png;base64...)**

1. The user poses a question to the RAG system.
2. The retrieval component searches the knowledge corpus using the question as a query and retrieves the most relevant passages or documents.
3. The retrieved content is passed to the LLM as additional context.
4. The language model processes the input and generates an answer by combining the information from the retrieved passages and its base knowledge.
5. The generated answer is returned to the user.

**Advantages of RAG**

1. **Expanded Knowledge**: Enables models to answer questions outside their training data by accessing an external corpus.
2. **Efficiency**: Reduces the size of the generative model by offloading knowledge storage to the retriever. It has faster response time.
3. **Dynamic Updates**: The knowledge base can be updated independently of the model, making the system adaptable.
4. **Explainability**: Provides insight into why a response was generated by exposing the retrieved documents.

**Example Use Cases:**

* Handling complex customer queries that require product manuals or FAQs. Retriever fetches sections from the product manual about resetting procedures.
* Summarizing medical guidelines or providing information about rare diseases. Retrievers pull information from medical journals or trusted health databases.
* Summarizing case laws or regulations for lawyers. Retriever finds case summaries and rulings from a legal database.

**RAG Python example with OpenSearch as backend**

**![Diagram of a software development process  Description automatically generated](data:image/png;base64...)**

**Step-1: Create Table (Index) in OpenSearch and Insert Embeddings**

**Add the following to the .env file**

OPENSEARCH\_HOST=localhost

OPENSEARCH\_PORT=9200

OPENSEARCH\_USERNAME=admin

OPENSEARCH\_PASSWORD=Opensearch#01

**Install Package**

pip install opensearch-py

**initialize\_db.py**

import os

from dotenv import load\_dotenv

from opensearchpy import OpenSearch

from opensearchpy.helpers import bulk

load\_dotenv()  # Load environment variables from .env file

from openai import OpenAI

openai\_client = OpenAI()

host = os.environ.get('OPENSEARCH\_HOST')

port = os.environ.get('OPENSEARCH\_PORT')

username = os.environ.get('OPENSEARCH\_USERNAME')

password = os.environ.get('OPENSEARCH\_PASSWORD')

# OpenSearch configuration dictionary

OPENSEARCH\_CONFIG = {

    "hosts": [{"host": host, "port": port}],

    "http\_auth": (username, password),

    "http\_compress": True,

    "use\_ssl": True,

    "verify\_certs": False,

    "ssl\_assert\_hostname": False,

    "ssl\_show\_warn": False

}

INDEX\_NAME = "funfacts"

# Mock documents array with fun facts

knowledge\_base = [

    {"content": "A group of flamingos is called a 'flamboyance'.", "name": "Fun Fact 1"},

    {"content": "Octopuses have five hearts.", "name": "Fun Fact 2"},

    {"content": "Butterflies taste with their feet.", "name": "Fun Fact 3"},

    {"content": "A snail can sleep for Five years.", "name": "Fun Fact 4"},

    {"content": "Elephants are the only animals that can't jump.", "name": "Fun Fact 5"},

    {"content": "A rhinoceros' horn is made of hair.", "name": "Fun Fact 6"},

    {"content": "Slugs have four noses.", "name": "Fun Fact 7"},

    {"content": "A cow gives nearly 200,000 glasses of milk in a lifetime.", "name": "Fun Fact 8"},

    {"content": "Bats are the only mammals that can fly.", "name": "Fun Fact 9"},

    {"content": "Koalas sleep up to 21 hours a day.", "name": "Fun Fact 10"}

]

# Function to return embedding array for the parameter arrayOfStrings using OpenAI Embedding API

def generate\_embeddings(arrayOfStrings):

    response = openai\_client.embeddings.create(input=arrayOfStrings, dimensions=1024, model="text-embedding-3-small")

    arrayOfEmbeddings = [item.embedding for item in response.data]

    return arrayOfEmbeddings

# Function to create OpenSearch index with knn\_vector mapping

def create\_opensearch\_index(opensearch\_client):

    index\_body = {

        "settings": {

                "index": {

                    "knn": True  # Enable k-NN

                },

        },

        "mappings": {

            "properties": {

                "id": {"type": "long"},  # ID field (similar to serial)

                "name": {"type": "text"}, # Text field for the document name

                "content": {"type": "text"}, # Text field for the document content

                "fact\_embedding": {

                    "type": "knn\_vector", # k-NN vector field for embeddings

                    "dimension": 1024, # Dimension of the embedding vector

                    "method": { # Method for indexing the embeddings

                        "name": "hnsw", # Hierarchical Navigable Small World Graph used for indexing

                        "space\_type": "cosinesimil", # Cosine similarity used for distance calculation (L2 for Euclidean Distance)

    # If you're working with text embeddings (like OpenSearch k-NN search), cosine similarity is usually the best choice.

                        "engine": "nmslib" # NMSLIB library used for indexing

                        }

                }

            }

        }

    }

    # Create the index (Table) if it does not exist

    if not opensearch\_client.indices.exists(INDEX\_NAME):

        opensearch\_client.indices.create(index=INDEX\_NAME, body=index\_body)

        print(f"Index '{INDEX\_NAME}' created.")

# Function to insert documents into OpenSearch

def insert\_documents(opensearch\_client, knowledge\_base, fact\_embeddings):

    actions = []

    for i, doc in enumerate(knowledge\_base):

        action = {

            "\_index": INDEX\_NAME,

            "\_id": i,

            "\_source": {

                "name": doc["name"],

                "content": doc["content"],

                "fact\_embedding": fact\_embeddings[i]

            }

        }

        actions.append(action)

    success, \_ = bulk(opensearch\_client, actions)

    print(f"Successfully inserted {success} documents into OpenSearch.")

# Main function to generate embeddings and insert documents

def main():

    # Extract contents from the documents

    arrayOfStrings = []

    for doc in knowledge\_base:

        arrayOfStrings.append(doc["content"])

    # Generate embeddings for the content

    arrayOfEmbeddings = generate\_embeddings(arrayOfStrings)

    # Connect to OpenSearch

    opensearch\_client = OpenSearch(\*\*OPENSEARCH\_CONFIG)

    # Create the OpenSearch index

    create\_opensearch\_index(opensearch\_client)

    # Insert documents with embeddings

    insert\_documents(opensearch\_client, knowledge\_base, arrayOfEmbeddings)

# Entry point of the script

if \_\_name\_\_ == "\_\_main\_\_":

    main()

**Open Search Operations**

**a) Get All Indices**

curl https://localhost:9200/\_cat/indices?v -u "admin:Opensearch#01" --insecure

**b) Get Contents Of Index Named Funfacts**

curl -X POST https://localhost:9200/funfacts/\_search -u "admin:Opensearch#01" --insecure --header "Content-Type: application/json" --data "{ \"query\": { \"match\_all\": {} }}" > demo.json

**c) Delete Index Named Funfacts**

curl -X DELETE https://localhost:9200/funfacts -u "admin:Opensearch#01" --insecure

**Step-2: Perform RAG Query on Filtered Data in Context.**

**rag.py**

import os

import numpy as np

from opensearchpy import OpenSearch

from create\_db import generate\_embeddings # Python file of Step-1

from openai import OpenAI

import os

openai\_client = OpenAI()

host = os.environ.get('OPENSEARCH\_HOST')

port = os.environ.get('OPENSEARCH\_PORT')

username = os.environ.get('OPENSEARCH\_USERNAME')

password = os.environ.get('OPENSEARCH\_PASSWORD')

# OpenSearch configuration

OPENSEARCH\_CONFIG = {

    "hosts": [{"host": host, "port": port}],

    "http\_auth": (username, password),

    "http\_compress": True,

    "use\_ssl": True,

    "verify\_certs": False,

    "ssl\_assert\_hostname": False,

    "ssl\_show\_warn": False

}

INDEX\_NAME = "funfacts"

# Function to retrieve documents from OpenSearch based on cosine similarity

def retrieve\_matching\_documents(opensearch\_client, user\_query, limit=3):

    # Generate the embedding for the query

    user\_query\_embedding = generate\_embeddings(user\_query)[0]

    # Perform the OpenSearch search to get all documents

    search\_body = {

        "\_source": ["content"],  # Only retrieve necessary fields

        "query": {

            "knn": {

                "fact\_embedding":{

                    "vector": user\_query\_embedding,

                    "k": limit,

                }

            }

        }

    }

    response = opensearch\_client.search(index=INDEX\_NAME, body=search\_body)

    # Extract documents and their embeddings

    documents\_string = ''

    # # match\_all query returns all documents, so we need to filter based on cosine similarity

    for hit in response["hits"]["hits"]:

        doc = hit["\_source"]

        documents\_string += doc['content']

    return documents\_string

# Function to interact with OpenAI and generate a response based on the retrieved documents

def generate\_chat\_response(user\_query, retrieved\_maching\_string):

    completion = openai\_client.chat.completions.create(

        model="gpt-4o-2024-08-06",

        messages=[

            #{"role": "system", "content": "You are a helpful assistant specialized about Animals. Provide your response base on information only in the context."},

            {"role": "system", "content": "You are a helpful assistant specialized about Animals. Provide your response including the information not necessary in the context."},

            {"role": "user", "content": f"Question: {user\_query}  \n Context: {retrieved\_maching\_string} "},

        ]

    )

    return completion.choices[0].message.content

# Main function for testing

def main():

    # User query for information

    user\_query = "I want to learn about animal sleep patterns"

    # Connect to OpenSearch

    opensearch\_client = OpenSearch(\*\*OPENSEARCH\_CONFIG)

    # Retrieve documents based on the user query

    retrieved\_maching\_string = retrieve\_matching\_documents(opensearch\_client, user\_query, limit=2)

    print('---------------------------------- Retrieved Documents ----------------------------------')

    for ele in retrieved\_maching\_string.split('.'):

        print(ele, sep='\n')

    print('---------------------------------------------------------------------------------------------------')

    if retrieved\_maching\_string:

        # Generate a response based on the retrieved documents

        response = generate\_chat\_response(user\_query, retrieved\_maching\_string)

        print("Response from OpenAI Assistant: ", response)

    else:

        print("No relevant documents found.")

if \_\_name\_\_ == "\_\_main\_\_":

    main()