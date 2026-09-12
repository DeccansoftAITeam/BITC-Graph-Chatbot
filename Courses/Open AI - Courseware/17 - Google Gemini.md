About Models

Models in Gemini: <https://ai.google.dev/gemini-api/docs/models>

pip install -q -U google-genai

Basic Example

from google import genai

client = genai.Client(api\_key="<KEY HERE>")

response = client.models.generate\_content(

    model="gemini-2.0-flash", contents="Explain how AI works in a few words"

)

print(response.text)

Streaming output

from google import genai

from dotenv import load\_dotenv

import os

load\_dotenv()

client = genai.Client(**api\_key=os.getenv("GEMINI\_API\_KEY"))**

response = client.models.**generate\_content\_stream**(

    model="gemini-2.0-flash",

    contents=["Explain how AI works"]

)

for chunk in response:

    print(chunk.text, end="")

Multi-turn Conversation

from google import genai

from dotenv import load\_dotenv

import os

load\_dotenv()

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

chat = client.chats.create(model="gemini-2.0-flash")

response = **chat.send\_message**("What is GenAI")

print(response.text)

print("-"\*100)

response = **chat.send\_message**("What are the features?")

print(response.text)

print("-"\*100)

print("-"\*100)

# To get all responses together

for message in **chat.get\_history():**

    print(f'role - {message.role}',end=": ")

    print(message.parts[0].text)

    print("-"\*100)

Configuration Parameters

Here are some of the model parameters you can configure. (Naming conventions vary by programming language.)

* **stopSequences**: Specifies the set of character sequences (up to 5) that will stop output generation. If specified, the API will stop at the first appearance of a stop\_sequence. The stop sequence won't be included as part of the response.
* **temperature**: Controls the randomness of the output. Use higher values for more creative responses, and lower values for more deterministic responses. Values can range from [0.0, 2.0].
* **maxOutputTokens**: Sets the maximum number of tokens to include in a candidate.
* **topP**: Changes how the model selects tokens for output. Tokens are selected from the most to least probable until the sum of their probabilities equals the topP value. The default topP value is 0.95.
* **topK**: Changes how the model selects tokens for output. A topK of 1 means the selected token is the most probable among all the tokens in the model's vocabulary, while a topK of 3 means that the next token is selected from among the 3 most probable using the temperature. Tokens are further filtered based on topP with the final token selected using temperature sampling

**Example:**

from google import genai

from google.genai import types

from dotenv import load\_dotenv

import os

load\_dotenv()

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

chat = client.chats.create(model="gemini-2.0-flash")

response = client.models.generate\_content(

    model="gemini-2.0-flash",

    contents=["Explain how AI works"],

    config=**types.GenerateContentConfig**(max\_output\_tokens=500,temperature=0.1, top\_p=0.8, top\_k=40, stop\_sequences=["\n"]),

)

print(response.text)

System Instructions

from google import genai

from google.genai import types

from dotenv import load\_dotenv

import os

load\_dotenv()

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

chat = client.chats.create(model="gemini-2.0-flash")

response = client.models.generate\_content(

    model="gemini-2.0-flash",

    config=types.GenerateContentConfig(**system\_instruction**="You are a cat. Your name is Minni."),

    contents=["What is your name?",

              "What is your favorite food?",

              "What is your favorite toy?",

              "What is your favorite thing to do?",],

)

print(response.text)

PDF Input

Gemini 1.5 Pro and 1.5 Flash support a maximum of 3,600 document pages.

Document pages must be in one of the following text data MIME types:

* PDF - application/pdf
* JavaScript - application/x-javascript, text/javascript
* Python - application/x-python, text/x-python
* TXT - text/plain
* HTML - text/html
* CSS - text/css
* Markdown - text/md
* CSV - text/csv
* XML - text/xml
* RTF - text/rtf

Each document page is equivalent to 258 tokens.

from google import genai

from google.genai import types

from dotenv import load\_dotenv

import os

load\_dotenv()

import httpx

load\_dotenv()

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

doc\_url = "https://discovery.ucl.ac.uk/id/eprint/10089234/1/343019\_3\_art\_0\_py4t4l\_convrt.pdf"

# Retrieve and encode the PDF byte

doc\_data = httpx.get(doc\_url).content

prompt = "Summarize this document"

response = client.models.generate\_content(

  model="gemini-2.0-flash",

  contents=[

      types.Part.from\_bytes(

        data=doc\_data,

        mime\_type='application/pdf',

      ),

      prompt])

print(response.text)

<https://ai.google.dev/gemini-api/docs/document-processing>

Structure Response

import json

import re

from google import genai

from google.genai import types

client = genai.Client(api\_key="AIzaSyBdYCECvGEi2PdKVdousRhZHj2Pb8wuzQc")

# The JSON Schema for a single review (used in the prompt)

review\_schema\_prompt = {

    "type": "object",

    "properties": {

        "product\_summary": {

            "type": "array",

            "items": {

                "type": "string",

                "description": "A brief summary of the product being reviewed."

            }

        },

        "rating": {

            "type": "number",

            "description": "The rating given to the product, usually on a scale from 1 to 5.",

            "minimum": 1,

            "maximum": 5

        },

        "rating\_text": {

            "type": "string",

            "description": "The text representation of the rating",

            "enum": ["excellent", "worst", "average", "not good", "good"]

        },

        "review\_text": {

            "type": "string",

            "description": "The detailed review text provided by the reviewer."

        },

        "reviewer": {

            "type": "string",

            "description": "The name or identifier of the reviewer."

        },

        "is\_review": {

            "type": "boolean",

            "description": "Indicates whether the input is a valid review or not. True if valid, False otherwise."

        }

    },

    "required": [

        "product\_summary",

        "rating",

        "review\_text",

        "reviewer",

        "is\_review",

        "rating\_text"

    ],

    "additionalProperties": False

}

# The JSON Schema for the list of reviews (used in the prompt)

**reviews\_schema\_prompt** = {

    "type": "object",

    "properties": {

        "reviews": {

            "type": "array",

            "items": review\_schema\_prompt,

        },

    },

    "required": ["reviews"],

    "additionalProperties": False,

}

# Example review text

user\_input = """

John rated Dell Laptop as excellent but also mentioned that Dell Mouse is average and Dell Keyboard as worst

Sandeep said samsung mobile is very good and he rated it as 4.5

Rahul gave negative feedback on the quality of the chair and rated it as 1.0

"""

# Construct the prompt to instruct Gemini to output JSON

prompt = f"""

Output the result as a JSON object that adheres to the following schema:

{json.dumps(reviews\_schema\_prompt, indent=2)}

Review Text: {user\_input}

"""

# Generate the response from Gemini

response = client.models.generate\_content(

            model='gemini-2.0-flash',

            config=types.GenerateContentConfig(system\_instruction="Extract the review details. Use NA for the missing fields. If a review is for more than one product, treat them as independent."),

            contents=prompt)

# Attempt to parse the JSON response

json\_string = response.text.strip()  # Remove leading/trailing whitespace

# Remove the ```json block if it exists

json\_string = re.sub(r"^\s\*```json\s\*", "", json\_string)

json\_string = re.sub(r"\s\*```\s\*$", "", json\_string)

rating\_json = json.loads(json\_string)

#print(rating\_json)

for review in rating\_json.get("reviews", []):

    print(f"Product Summary: {review.get('product\_summary', 'NA')}")

    print(f"Rating: {review.get('rating', 'NA')}")

    print(f"Rating Text: {review.get('rating\_text', 'NA')}")

    print(f"Review Text: {review.get('review\_text', 'NA')}")

    print(f"Reviewer: {review.get('reviewer', 'NA')}")

    print(f"Is Review: {review.get('is\_review', 'NA')}")

    print("-" \* 20)

Pydantic Example:

from pydantic import BaseModel, Field

from typing import List, Literal

from dotenv import load\_dotenv

from google import genai

import os

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

load\_dotenv()

class **Review(BaseModel):**

    product\_summary: List[str] = Field(..., description="A brief summary of the product being reviewed." )

    rating: float = Field(...,description="The rating given to the product, usually on a scale from 1 to 5.",)

    rating\_text: Literal["excellent", "good", "average", "not good", "worst"] = Field(..., description="The text representation of the rating.")

    review\_text: str = Field(..., description="The detailed review text provided by the reviewer.")

    reviewer: str = Field(..., description="The name or identifier of the reviewer.")

    is\_review: bool = Field(...,description="Indicates whether the input is a valid review or not. True if valid, False otherwise.",    )

response = client.models.generate\_content(

    model="gemini-2.0-flash",

    contents="List a few popular cookie recipes. Be sure to include the amounts of ingredients.",

    config={

        "response\_mime\_type": "application/json",

        "response\_schema": list[Review],

    },

)

# Use instantiated objects.

my\_reviews: list[Review] **= response.parsed**

for rating in my\_reviews:

    print(f"Product Summary: {rating.product\_summary}")

    print(f"Rating: {rating.rating}")

    print(f"Rating Text: {rating.rating\_text}")

    print(f"Review Text: {rating.review\_text}")

    print(f"Reviewer: {rating.reviewer}")

    print(f"Is Review: {rating.is\_review}")

    print("-" \* 20)

Embeddings

The Gemini API offers three models that generate text embeddings:

[gemini-embedding-exp-03-07](https://ai.google.dev/gemini-api/docs/models#gemini-embedding)

[text-embedding-004](https://ai.google.dev/gemini-api/docs/models/gemini#text-embedding)

[embedding-001](https://ai.google.dev/gemini-api/docs/models/gemini#embedding)

Example:

from google import genai

from google.genai import types

from numpy import dot

from numpy.linalg import norm

def cosine\_similarity(vector1, vector2):

    return dot(vector1, vector2) / (norm(vector1) \* norm(vector2))

client = genai.Client(api\_key="AIzaSyBdYCECvGEi2PdKVdousRhZHj2Pb8wuzQc")

result = **client.models.embed\_content**(

    model="gemini-embedding-exp-03-07",

    contents=["I love AI?", "I have AI"],

    config=types.EmbedContentConfig(output\_dimensionality=5),

)

print(result.embeddings[0].values)

print(result.embeddings[1].values)

Function Calling

from pydantic import BaseModel, Field

from typing import List, Literal

from dotenv import load\_dotenv

from google import genai

from google.genai import types

import os

import json

import requests

load\_dotenv()

client = genai.Client(api\_key=os.getenv("GEMINI\_API\_KEY"))

# \*\*\*\*\*\*\*\*\*Step1: Create a function to get the weather\*\*\*\*\*\*\*\*\*

# The function will take latitude and longitude as input and return the current temperature in celsius.

def **get\_weather**(latitude, longitude):

    response = requests.get(

        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature\_2m,wind\_speed\_10m&hourly=temperature\_2m,relative\_humidity\_2m,wind\_speed\_10m"

    )

    data = response.json()

    return data["current"]["temperature\_2m"]

get\_weather\_schema = {

    "name": "get\_weather",

    "description": "Get current temperature for provided coordinates in celsius.",

    "parameters": {

        "type": "object",

        "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},

        "required": ["latitude", "longitude"],

    },

}

# Replace with your API keys

news\_api\_key = "c86245eca72141828e351e1ea1e92fae"

# Define the `get\_news` function to retrieve news articles based on a given topic

def get\_news(topic):

    print(f"In get news about {topic}")

    url = (

        f"https://newsapi.org/v2/everything?q={topic}&apiKey={news\_api\_key}&pageSize=5"

    )

    try:

        response = requests.get(url)

        if response.status\_code == 200:

            news = json.dumps(response.json(), indent=4)

            news\_json = json.loads(news)

            # Access all the fields == loop through

            status = news\_json["status"]

            total\_results = news\_json["totalResults"]

            articles = news\_json["articles"]

            final\_news = []

            # Loop through articles

            for article in articles:

                source\_name = article["source"]["name"]

                author = article["author"]

                title = article["title"]

                description = article["description"]

                url = article["url"]

                content = article["content"]

                title\_description = f"""

                   Title: {title},

                   Author: {author},

                   Source: {source\_name},

                   Description: {description},

                   URL: {url},

                   Content: {content}

                """

                final\_news.append(title\_description)

            return final\_news

        else:

            return []

    except requests.exceptions.RequestException as e:

        return f"Error occurred during API Request: {e}"

# Define the function schema for OpenAI API

get\_news\_function\_schema = {

    "name": "get\_news",

    "description": "Retrieve the latest news articles on a given topic.",

    "parameters": {

        "type": "object",

        "properties": {

            "topic": {

                "type": "string",

                "description": "The topic to search news articles for.",

            }

        },

        "required": ["topic"],

    },

}

# Generation Config with Function Declaration

**tools** = types.Tool(function\_declarations=[get\_weather\_schema,get\_news\_function\_schema])

**config** = types.GenerateContentConfig(tools=[tools])

contents = [

    types.Content(

        role="user", parts=[types.Part(text="What's the clothing suitable for the weather in Hyderabad (Latitude=17.38, Langitude=78.48). Also include the news of Hyderabad about AI.")]

    )

]

chat = client.chats.create(model="gemini-2.0-flash", config=config)

response = client.models.generate\_content(

    model="gemini-2.0-flash",

    contents=contents,

    config=**config**,

)

# \*\*\*\*\*\*\*\*\*Step3: Model decides to call function(s) – model returns the name and input arguments.\*\*\*\*\*\*\*\*\*

# Extract the arguments from the function

for fn in response.function\_calls:

    #    tool\_call = completion.choices[0].message.tool\_calls[0]

    args = fn.args

    print("Function Name: ", fn.name, " Arguments ", args)

    if fn.name == "get\_news":

        result = get\_news(args["topic"])

    elif fn.name == "get\_weather":

        result = get\_weather(args["latitude"], args["longitude"])

    # Create a function response part

    function\_response\_part = types.Part.from\_function\_response(

        name=fn.name,

        response={"result": result},

    )

    # Append function call and result of the function execution to contents

    contents.append(

        types.Content(

            role="model", parts=[types.Part(function\_call=fn)]

        )

    )  # Append the model's function call message

    contents.append(

        types.Content(role="user", parts=[function\_response\_part])

    )  # Append the function response

response\_2 = client.models.generate\_content(

    model="gemini-2.0-flash",

    contents=contents,

    config=config,

)

print(response\_2.text)