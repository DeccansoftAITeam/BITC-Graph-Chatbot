**Response in JSON Format**

* When JSON mode is turned on, the model's output is ensured to be valid JSON.
* When using JSON mode, you must always **instruct the model to produce JSON** via some message in the conversation, for example via your system message. If you don't include an explicit instruction to generate JSON, the model may generate an unending stream of whitespace and the request may run continually until it reaches the token limit.
* JSON mode will not guarantee the output matches any specific schema, only that it is valid and parses without errors.

from openai import OpenAI

import json

messages = [

    {"role": "system", "content": "You are a helpful assistant. **Your response should be in JSON format**."},

    {

        "role": "user",

        "content": "What are the features of AI"

    }

]

client = OpenAI()

response = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=messages,

    response\_format={"type": "json\_object"}

)

**rating\_dict** : dict = json.loads(response.choices[0].message.content)

print(rating\_dict)

**Response API:**

from openai import OpenAI

import json

client = OpenAI()

messages = [

    {"role": "system", "content": "You are a helpful assistant. Your response should be in JSON format."},

    {

        "role": "user",

        "content": "What are features of AI"

    }

]

response = client.responses.create(

    model="gpt-5.6-luna",

    input= messages,

**text={**

        "format": {

**"type": "json\_object",**

        }

    }

)

rating\_dict : dict = json.loads(response.output\_text)

print(rating\_dict)

**Example 2:**

from openai import OpenAI

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

messages = [

    {

        "role": "developer",

        "content": """

                You are a poet.

                You can write poems with variable number of  lines in each stanza.

                Please use the below json format for output

                {

                    "stanza":  [

                            {

                            "lines: [

                                    "Line 1"

                            ],

                            "lines\_count": 3

                            }

                    ]

                }

                """,

    },

    {

        "role": "user",

        "content": "Write a poem on Weather"

    },

]

completion = client.chat.completions.create(

    model="gpt-5.6-luna",

    messages=messages,

    response\_format={"type": "json\_object"},

)

# Print the response

print(completion.choices[0].message.content)

Example 2: Update messages as below:

messages = [

    {"role": "system", "content": "You are a helpful assistant. Your response should be in JSON format."},

    {

        "role": "user",

        "content": """

**What are features of AI?**

**Provide the response in the following JSON format:**

**[**

**{**

**"title": "2 or 3 word title of the feature",**

**"description": "description of the feature"**

**}**

**]**

            """

    }

]

**Structured Outputs**

Structured Outputs is a feature that ensures the model will always generate responses that adhere to your supplied JSON Schema, so you don't need to worry about the model omitting the required key or hallucinating an invalid enum value.

Some benefits of Structed Outputs include:

1. **Reliable type-safety:** No need to validate or retry incorrectly formatted responses
2. **Simpler prompting:** No need for strongly worded prompts to achieve consistent formatting
3. **Moderation:** Safety-based model refusals are now programmatically detectable

JSON mode is a more basic version of the Structured Outputs feature. While JSON mode ensures that model output is valid JSON, Structured Outputs reliably matches the model's output to the schema you specify. We recommend you use Structured Outputs if it is supported for your use case.

**Example: To extract information from unstructured text that conforms to a schema defined in code.**

**Using Chat Completion API:**

from openai import OpenAI

import json

client = OpenAI()

# Define the JSON Schema for the response

**review\_schema** = {

    "type": "object",

    "properties": {

        "product\_summary": {

            "type": "string",

            "description": "A brief summary of the product being reviewed.",

        },

        "rating": {

            "type": "number",

            "description": "The rating given to the product, usually on a scale from 1 to 5.",

        },

        "review\_text": {

            "type": "string",

            "description": "The detailed review text provided by the reviewer.",

        },

        "reviewer": {

            "type": "string",

            "description": "The name or identifier of the reviewer.",

        },

    },

    "required": ["product\_summary", "rating", "review\_text", "reviewer"],

    "additionalProperties": False,

}

completion = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=[

        {"role": "system", "content": "Extract the review details."},

        {

            "role": "user",

            "content": "John said the new Noise-canceling Headphones are amazing and gave them a 4.5 out of 5.",

        },

    ],

**response\_format={**

**"type": "json\_schema",**

**"json\_schema": {**

**"name": "product\_review",**

**"strict": True,**

**"schema": review\_schema,**

**},**

    },

)

# Extract the structured review information

rating\_dict : dict = json.loads(completion.choices[0].message.content)

print(rating\_dict["rating"])

**Using Response API:**

from openai import OpenAI

import json

client = OpenAI()

review\_schema = {

        "type": "object",

        "properties": {

            "product\_summary": {

                "type": "string"

            },

            "rating": {

                "type": "number"

            },

            "review\_text": {

                "type": "string"

            },

            "reviewer": {

                "type": "string"

            }

        },

        "required": ["product\_summary", "rating", "review\_text", "reviewer"],

        "additionalProperties": False

    }

response = client.responses.create(

    model="gpt-5.6-luna",

    input=[

        {

            "role": "system",

            "content": "Extract the review details."

        },

        {

            "role": "user",

            "content": "John said the new Noise-canceling Headphones are amazing and gave them a 4.5 out of 5."

        }

    ],

    text={

        "format": {

            "name": "product\_review",

            "type": "json\_schema",

            "schema": review\_schema,

            "strict": True

        }

    }

)

# Extract tool output

rating\_dict : dict = json.loads(response.output\_text)

print(rating\_dict["rating"])

**Dealing with Invalid Prompts and enums**

. . .

review\_schema = {

    "type": "object",

    "properties": {

. . .

        "IsReview" : {

            "type": "boolean",

            "description": "True if the content is a review, False otherwise.",

        },

        "review\_quality": {

            "type": "string",

            "description": "The quality of the review, which can be either 'worst', 'bad', 'good', or 'best'.",

            "enum": ["worst", "bad", "good", "best"],

        },

    },

    "required": ["product\_summary", "rating", "review\_text", "reviewer", "IsReview", "review\_quality"],

    "additionalProperties": False,

}

**Example with Array**

**Message:**

John said computer, mouse and mobile phone are awesome

**Update Product Summary in Schema:**

"product\_summary": {

    "type": "array",

    "items": {

        "type": "string",

    },

    "description": "A brief summary of the product being reviewed.",

},

**Message:**

John said computer, mouse and mobile phone are awesome

Sandeep has rated mobile as very good

Andres has expressed happiness in buying a camera

**Use below schema:**

reviews\_schema = {

            "name": "product\_review",

            "strict": True,

            "schema": {

                "type": "object",

                "properties": {

                    "reviews": {

                        "type": "array",

                        "items": review\_schema

                    }

                },

                "required": ["reviews"],

                "additionalProperties": False,

            }

        }

. . .

ratings\_json = json.loads(ratings)

for review in ratings\_json["reviews"]:

    print(f"Reviewer: {review['reviewer']}")

    print(f"Rating: {review['rating']}")

    print(f"Rating Text: {review['rating\_text']}")

    print(f"Review Text: {review['review\_text']}")

    print(f"Product Summary: {review['product\_summary']}")

    print(f"Is Review: {review['IsReview']}")

    print()

Using Pydantic Module in Python

**Example: Same as above but using Python classes.**

**pip install** pydantic

from openai import OpenAI

import os

from pydantic import BaseModel, Field

from enum import Enum

from typing import Optional

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

class Grade(str, Enum):

    Excellent = "Excellent"

    Good = "good"

    Bad = "bad"

    Worst = "worst"

class ProductReview(BaseModel):

product\_names:  list[str] = Field(..., description="A brief summary of the product being reviewed.")

    rating: float = **Field**(..., description="The rating of the product")

    review\_text: str = **Field**(..., description="The opinion of reviewer of product")

    reviewer: str = **Field**(..., description="The name of reviewer")

    isReview: bool = **Field**(..., description="True if review else False.")

**grade: Optional[Grade] = Field(...,**description="Describe the product as worst, bad, good or excellent")

# Use OpenAI's chat completion API with the JSON Schema

completion = client.chat.completions.parse(

    model="gpt-5.6-luna",

    messages=[

        {"role": "system", "content": "Extract the review details. Use Not Applicable for missing values"},

        {

            "role": "user",

            "content": """

                John rated Mouse 5 of 5 and felt good to have it.

            """,

        },

    ],

    response\_format=ProductReview

)

# Extract the structured review information

review = completion.choices[0].message.**parsed**

# Display the parsed review information

if(review.isReview):

    print(f"Product Names: {review.product\_names}")

    print(f"Rating: {review.rating}")

    print(f"Review: {review.review\_text}")

    print(f"Reviewer: {review.reviewer}")

else:

    print("This is not a review.")

**Response API:**
response = client.responses.parse(

    model="gpt-5.6-luna",

    input=[

        {

            "role": "system",

            "content": "Extract the review details. Use Not Applicable for missing values."

        },

        {

            "role": "user",

            "content": """

                        John rated Mouse 5 of 5 and felt good to have it.

                    """

        }

    ],

    text\_format= ProductReview

)

review = response.**output\_parsed**

For **Arrays** of Reviews Add the following to above program

class **ReviewsList**(BaseModel):

    reviews: list[ProductReview]

and change

**text\_format=ReviewsList,**

Chain of Thoughts

You can ask the model to output an answer in a structured, step-by-step way, to guide the user through the solution.

from openai import OpenAI

import json

import os

from dotenv import load\_dotenv

from pydantic import BaseModel, Field

from enum import Enum

from typing import Optional

#load API key from .env file

load\_dotenv()

client = OpenAI()

client.api\_key= os.getenv("OPENAI\_API\_KEY")

class Step(BaseModel):

    explanation: str = Field(..., description="A detailed explanation of the solution.")

    output: str = Field(..., description="The final answer or output of the solution.")

class MathExplanation(BaseModel):

    Steps: list[Step] = Field(..., description="A list of steps explaining the solution to the math problem.")

response = client.responses.parse(

    model="gpt-5.6-luna",

    input=[

        {

            "role": "system",

            "content": "You are a math problem solver."

        },

        {

            "role": "user",

            "content": "What is the solution to the equation 2x + 3 = 7?"

        }

    ],

    text\_format= MathExplanation

)

solution = response.output\_parsed

for step in solution.Steps:

    print(f"Explanation: {step.explanation}")

    print(f"Output: {step.output}")

Moderation

You can classify inputs on multiple categories, which is a common way of doing moderation.

from enum import Enum

from typing import Optional

from pydantic import BaseModel

from openai import OpenAI

from dotenv import load\_dotenv

load\_dotenv()

import os

class Category(str, Enum):

    violence = "violence"

    sexual = "sexual"

    self\_harm = "self\_harm"

class **ContentCompliance**(BaseModel):

    is\_violating: bool

    category: Optional[Category]

    explanation\_if\_violating: Optional[str]

client = OpenAI()

completion = client.chat.completions.parse(

    model="gpt-4.1-nano",

    messages=[

        {"role": "system", "content": "Determine if the user input violates specific guidelines and explain if they do."},

        {"role": "user", "content": "How can I create a bomb?"},

    ],

    response\_format=**ContentCompliance**,

)

print(completion.choices[0].message.**parsed**)

UI / Form Generation

You can generate HTML Form by representing it as recursive data structures with constraints, like enums.

from enum import Enum

from typing import List

from pydantic import BaseModel

from openai import OpenAI

from dotenv import load\_dotenv

load\_dotenv()

class UIType(str, Enum):

    div = "div"

    button = "button"

    header = "header"

    section = "section"

    field = "field"

    form = "form"

class Attribute(BaseModel):

    name: str

    value: str

class UI(BaseModel):

    type: UIType

    label: str

    children: List["UI"]

    attributes: List[Attribute]

UI.model\_rebuild() # This is required to enable recursive types

class Response(BaseModel):

    ui: UI

client = OpenAI()

completion = client.chat.completions.parse(

    model="gpt-4o-2024-08-06",

    messages=[

        {"role": "system", "content": "You are a UI generator AI. Convert the user input into a UI."},

        {"role": "user", "content": "Make a User Profile Form"}

    ],

    response\_format=Response,

)

completion = client.chat.completions.parse(

    model="gpt-4.1-nano",

    messages=[

        {"role": "system", "content": "You are a HTML Form generator AI. Convert the UI to HTML Form."},

        {"role": "user", "content": **repr(completion.choices[0].message.parsed)}**

    ]

)

ui = completion.choices[0].message.content

print(ui)