Web search

Allow models to search the web for the latest information before generating a response.

Currently, you need to use one of these models to use web search in Chat Completions:

* gpt-4o-search-preview
* gpt-4o-mini-search-preview

**Chat Completion API**

from openai import OpenAI

client = OpenAI()

completion = **client.chat.completions.create**(

    model="gpt-4o-search-preview",

    web\_search\_options={},

    messages=[

        {

            "role": "user",

            "content": "What was a positive news story from today?",

        }

    ],

)

print(completion.choices[0].message.content)

**Resposne API:**

from openai import OpenAI

client = OpenAI()

response = client.responses.create(

    model="gpt-5",

    tools=[{"type": "web\_search"}],

    input="What was a positive news story from today?"

)

print(response.output\_text)

**User location:**

* To refine search results based on geography, you can specify an approximate user location using country, city, region, and/or timezone.
* The city and region fields are free text strings, like Minneapolis and Minnesota respectively.
* The country field is a two-letter [ISO country code](https://en.wikipedia.org/wiki/ISO_3166-1), like US.
* The timezone field is an [IANA timezone](https://timeapi.io/documentation/iana-timezones) like America/Chicago

**Search context size:**

It controls how much context is retrieved from the web to help the tool formulate a response.

* **Cost**: Pricing of our search tool varies based on the value of this parameter. Higher context sizes are more expensive (https://platform.openai.com/docs/pricing).
* **Quality**: Higher search context sizes generally provide richer context, resulting in more accurate, comprehensive answers.
* **Latency**: Higher context sizes require processing more tokens, which can slow down the tool's response time.

from openai import OpenAI

client = OpenAI()

completion = client.chat.completions.create(

    model="gpt-4o-search-preview",

    web\_search\_options={

        "search\_context\_size": "low",

        "user\_location": {

            "type": "approximate",

            "approximate": {

                "country": "IN",

                "city": "Secunderabad",

                "region": "Secunderabad",

            },

        }

    },

    messages=[

        {

            "role": "user",

            "content": "What was a positive news story from today in my location?",

        }

    ],

)

print("Content: ", completion.choices[0].message.content)

print("Title: ", completion.choices[0].message.annotations[0].url\_citation.title)

print("URL: ", completion.choices[0].message.annotations[0].url\_citation.url)

Using function calling with OpenAI Service

* Function calling is useful when you are building an application that **bridges the models and functionality of your application**. For example, you can give the model access to functions that query a database in order to build an AI assistant that can help users with their orders, or functions that can interact with the UI.
* The latest versions of gpt-35-turbo and gpt-4 are fine-tuned to work with functions and are able to both determine when and how a function should be called.
* If one or more functions are included in your request, the model determines if any of the functions should be called based on the context of the prompt.
* When the model determines that a function should be called, it responds with a JSON object including the arguments for the function.

At a high level you can break down working with functions into three steps:

1. Call the chat completions API with **your functions** and **the user query**
2. Use the model’s response to call your API or function.
3. Call the chat completions API again, including the response from your function to get a final response.

![Function Calling Diagram Steps](data:image/png;base64...)

**Tool choice:** By default the model will determine when and how many tools to use. You can force specific behavior with the **tool\_choice** parameter.

1. **Auto:** (*Default*) Call zero, one, or multiple functions. **tool\_choice: "auto"**
2. **Required:** Call one or more functions. **tool\_choice: "required"**
3. **Forced Function:** Call exactly one specific function. **tool\_choice: {"type": "function", "function": {"name": "get\_weather"}}**
4. **None:** Imitate the behavior of passing no functions.

**Note: If the model decides that no function should be called, then the response will contain a direct reply to the user as a regular chat completion response.**

**Strict mode:** Setting strict to true will ensure function calls reliably adhere to the function schema, instead of being best effort. We recommend always enabling strict mode.

Notes: <https://platform.openai.com/docs/guides/function-calling?example=get-weather&strict-mode=disabled#additional-configurations>

Single tool/function calling example

import requests

import json

from openai import OpenAI

client = OpenAI()

#\*\*\*\*\*\*\*\*\*Step1: Create a function to get the weather\*\*\*\*\*\*\*\*\*

# The function will take latitude and longitude as input and return the current temperature in celsius.

def **get\_weather**(latitude, longitude):

    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature\_2m,wind\_speed\_10m&hourly=temperature\_2m,relative\_humidity\_2m,wind\_speed\_10m")

    data = response.json()

    return data['current']['temperature\_2m']

#\*\*\*\*\*\*\*\*\*Step2: Call model with functions defined – along with your system and user messages.\*\*\*\*\*\*\*\*

**get\_weather\_schema** = {

        "**name**": "get\_weather",

        "description": "Get current temperature for provided coordinates in celsius.",

        "**parameters**": {

            "type": "object",

            "properties": {

                "latitude": {"type": "number"},

                "longitude": {"type": "number"}

            },

            "required": ["latitude", "longitude"],

            "additionalProperties": False

        },

        "strict": True

    }

tools = [{

    "type": "function",

    "function": get\_weather\_schema

}]

messages = [{"role": "user", "content": "What's the best clothing based on weather in Paris today?"}]

completion = client.chat.completions.create(

    model="gpt-4o",

    messages=messages,

    tools=tools

)

messages.append(completion.choices[0].message)  # append model's function call message

#\*\*\*\*\*\*\*\*\*Step3: Model decides to call function(s) – model returns the name and input arguments.\*\*\*\*\*\*\*\*\*

# Extract the arguments from the function

tool\_call = completion.choices[0].message.tool\_calls[0]

args = json.loads(tool\_call.function.arguments)

print(tool\_call.function.name)

print(args)

#\*\*\*\*\*\*\*\*Step 4: Execute function code – parse the model's response and handle function calls.\*\*\*\*\*\*\*\*\*

result = **get\_weather**(args["latitude"], args["longitude"])

#\*\*\*\*\*\*\*\*Step 5: Supply model with results – so it can incorporate them into its final response.\*\*\*\*\*\*\*\*\*

messages.append({   # append result message

    "role": "**tool**",

    "tool\_call\_id": tool\_call.id,

    "content": str(result)

})

completion\_2 = client.chat.completions.create(

    model="gpt-4o",

    messages=messages,

    tools=tools,

)

print(completion\_2.choices[0].message.content)

Note: The the query to "What's the weather like in Paris and Delhi today?" and run the application again. Note that it throws error as tool call result for Delhi is missing

Example2: Calling Same function multiple times

import requests

import json

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

def get\_weather(latitude, longitude):

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

        "additionalProperties": False,

    },

    "strict": True,

}

tools = [{"type": "function", \*\*get\_weather\_schema}]

inputs = [

    {

        "role": "user",

        "content": "What's the best clothing based on weather in Paris and Mumbai today?",

    }

]

previous\_response\_Id = None

while True:

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=inputs,

        previous\_response\_id=previous\_response\_Id,

        tools=tools,

    )

    previous\_response\_Id = response.id

    if response.output\_text:

        print(response.output\_text)

        break

    inputs = []

    for item in response.output:

        if item.type == "function\_call":

            args = json.loads(item.arguments)

            print(item)

            print(args)

            if item.name == "get\_weather":

                result = get\_weather(args["latitude"], args["longitude"])

            inputs.append(

                {

                    "type": "function\_call\_output",

                    "call\_id": item.call\_id,

                    "output": str(result),

                }

            )

Multiple functions calling

**Example with Weather and News**

import requests

import json

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

def **get\_weather**(latitude, longitude):

    response = requests.get(

        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature\_2m,wind\_speed\_10m&hourly=temperature\_2m,relative\_humidity\_2m,wind\_speed\_10m"

    )

    data = response.json()

    return data["current"]["temperature\_2m"]

**get\_weather\_schema** = {

    "name": "get\_weather",

    "description": "Get current temperature for provided coordinates in celsius.",

    "parameters": {

        "type": "object",

        "properties": {"latitude": {"type": "number"}, "longitude": {"type": "number"}},

        "required": ["latitude", "longitude"],

        "additionalProperties": False,

    },

    "strict": True,

}

# Define the `get\_news` function to retrieve news articles based on a given topic

news\_api\_key = "c86245eca72141828e351e1ea1e92fae"

def **get\_news**(topic):

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

**get\_news\_schema** = {

        "name": "get\_news",

        "description": "Get news articles based on a given topic.",

        "parameters": {

            "type": "object",

            "properties": {

                "topic": {"type": "string"}

            },

            "required": ["topic"],

            "additionalProperties": False

        },

        "strict": True

    }

tools = [{"type": "function", \*\*get\_weather\_schema}, {"type": "function", \*\*get\_news\_schema}]

inputs = [

    {

        "role": "user",

        "content": "What's the best clothing based on weather in Paris and Mumbai today? Also let me know the latest news about these cities.",

    }

]

previous\_response\_Id = None

while True:

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=inputs,

        previous\_response\_id=previous\_response\_Id,

        tools=tools,

    )

    previous\_response\_Id = response.id

    if response.output\_text:

        print(response.output\_text)

        break

    inputs = []

    for item in response.output:

        if item.type == "function\_call":

            args = json.loads(item.arguments)

            if item.name == "get\_weather":

                result = get\_weather(args["latitude"], args["longitude"])

            elif item.name == "get\_news":

                result = get\_news(args["topic"])

            inputs.append(

                {

                    "type": "function\_call\_output",

                    "call\_id": item.call\_id,

                    "output": str(result),

                }

            )

Using Code Interpreter Tool

from openai import OpenAI

import os

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

response = client.responses.create(

    model="gpt-5.2",

    input="""

Use Python to compute:

1) mean of [10, 20, 30, 40, 50]

2) standard deviation

Then explain the result in one short sentence.

""",

    tools=[

        {

            "type": "code\_interpreter",

            "container": {"type": "auto"}

        }

    ],

)

print(response.output\_text)

**Example with Custom Python Code:**

from openai import OpenAI

import os

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

my\_code = """

import math

values = [10, 20, 30, 40, 50]

mean = sum(values) \* 0 / len(values)

variance = sum((x - mean) \*\* 2 for x in values) / len(values)

std\_dev = math.sqrt(variance)

print("mean:", mean)

print("std\_dev:", std\_dev)

"""

resp = client.responses.create(

    model="gpt-5.2",

    tools=[{"type": "code\_interpreter", "container": {"type": "auto"}}],

    input=f"Run this Python code and return the printed output only:\n\n```python\n**{my\_code**}\n```"

)

print(resp.output\_text)