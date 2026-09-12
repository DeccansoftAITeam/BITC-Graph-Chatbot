**Getting Started with OpenAI API**

* Setup OpenAI API Account
* Access OpenAI Service / API Security
* Use OpenAI API Platform
* Calling Completion API using HTTP REST calls
  + Curl
  + Python
* Completion API
  + Using Python SDK
* Prompt with System, User and Assistant Message

Setup OpenAI API Account

OpenAI provides simple APIs to use a large language model to generate text from a prompt, as you might using ChatGPT.

![A diagram of a computer  AI-generated content may be incorrect.](data:image/png;base64...)

**Supported APIs:**

1. **Chat Completions API (/v1/chat/completions)**: The traditional Chat Completions API remains supported for backward compatibility but is no longer the recommended approach for new projects, especially with reasoning models.
2. **Response API** (**/v1/responses**): The Responses API represents a new approach to interacting with OpenAI models, designed specifically for building agents and using tools.
3. **Embeddings API (/v1/embeddings)** : Convert text into vector representations for semantic search, clustering, classification, or retrieval-augmented generation (RAG).
4. **Image API (/v1/images/)**: Generate, edit, or create variations of images based on prompts.
5. **Batch API**: Allows for the processing of multiple requests in a single call, enhancing efficiency in handling large volumes of data.
6. **Moderation API (**/v1/moderations)**:** Check text (and sometimes images) for harmful, unsafe, or policy-violating content.
7. **Audio & Speech Endpoints:** Speech-to-text transcription and text-to-speech

**Configure your account:**

1. Go to <https://platform.openai.com/> 🡪 Settings 🡪 General
2. Update Organization Name
3. ORGANIZATION:
   1. Members 🡪 + Invite 🡪 Invite members from your organization
   2. Project 🡪 + Create 🡪 Project name = "MySampleProject"
4. PROJECT:
   1. Members 🡪 + Add member
   2. Limits 🡪 Set Budget Alerts, Budget Limit, Model usage, Rate limits
   3. Models 🡪 List of allowed or denyed models.

**Authentication:**

The OpenAI API uses API keys for authentication. You can create API keys at a **user** or **service account** level.

* **User Level** API key is tied to user and can make requests against the selected project. If a user is removed from the organization or project, key will be disabled.
* **Service accounts Level** is tied to new bot member (service account) created in the project. Should be used to provision access for production systems.

Note: Do not share your API key with others or expose it in the browser or other client-side code. To protect your account's security, OpenAI may automatically disable any API key that has leaked publicly.

**Create an API key:**

1. Go to <https://platform.openai.com/> 🡪 Settings 🡪
2. PROJECT:
3. Members 🡪 + Add member
4. API Keys 🡪 Create new secret key 🡪 Name=MyTestKey, Project=MySampleProject, Permissions=All 🡪 Create secret key
5. Copy the Key and store it in a secured location. (It cannot be viewed later)

Example using Curl

**Endpoint for Chat Completion**

Default Open AI: [https://api.openai.com**/v1/chat/completions**](https://api.openai.com/v1/chat/completions)

All API requests should include your API key in an Authorization HTTP header as follows:

Authorization: Bearer <OPENAI\_API\_KEY>

**Split into multiple lines for understanding:**

# curl -X POST "https://api.openai.com/v1/chat/completions"

-H "Content-Type: application/json"

-H "Authorization: Bearer **<API TOKEN>**"

-d "{

\"model\":\"gpt-5.6-luna \",

\"messages\":[

{

\"role\":\"user\",

\"content\":\"What is OpenAI\"

}

]

}"

**One line statement:**

curl -X POST https://api.openai.com/v1/chat/completions -H "Authorization: Bearer **<TOKEN GOES HERE>**" -H "Content-Type: application/json" -d **"{\"model\": \"gpt-5.6-luna-\", \"messages\": [{\"role\": \"user\", \"content\": \"What is OpenAI?\"}]}"** ~~--ssl-no-revoke~~

**o/p schema:**

{

"id": "chatcmpl-Afibl2v6tjYD6HPkuAHt1m6QGJrGX",

"object": "chat.completion",

"created": 1734506285,

"model": "gpt-5.6-luna",

"**choices**": [

{

"index": 0,

"**message**": {

"role": "assistant",

"content": "OpenAI is an artificial . . . and commercial partnerships.",

"refusal": null

},

"logprobs": null,

"finish\_reason": "stop"

}

],

"**usage**": {

"prompt\_tokens": 11,

"completion\_tokens": 160,

"total\_tokens": 171,

"prompt\_tokens\_details": {

"cached\_tokens": 0,

"audio\_tokens": 0

},

"completion\_tokens\_details": {

"reasoning\_tokens": 0,

"audio\_tokens": 0,

"accepted\_prediction\_tokens": 0,

"rejected\_prediction\_tokens": 0

}

},

"**system\_fingerprint**": "fp\_6fc10e10eb"

}

1. **finish\_reason:** Reason why the completion stopped.
   * "stop": Stopped naturally (e.g., the model finished generating).
   * "length": Stopped because the token limit was reached.
   * "content\_filter": Stopped due to a content filter.
   * "null": Incomplete or unknown stop reason.
2. **prompt\_tokens**: Number of tokens used in the input prompt.
3. **Completion\_tokens**: Number of tokens used in the output (response).
4. **total\_tokens**: Total number of tokens used (input + output).
5. **refusal**: Indicates if a refusal to generate content occurred. (Null or reason string)

* **cached\_tokens**: Tokens reused from cache for efficiency.
* **audio\_tokens**: Tokens generated for audio inputs.
* **reasoning\_tokens**: Tokens generated for logical reasoning in responses.
* **audio\_tokens**: Tokens associated with audio-based responses.
* **accepted\_prediction\_tokens**: Tokens accepted as part of the final response.
* **rejected\_prediction\_tokens**: Tokens generated but not included in the final response.
* **system\_fingerprint:** uniquely identifying system settings or configurations.

Set OpenAI Environment Variable in Windows

1. Open Powershell

Windows Start 🡪 Powershell

1. Set for current user:

[Environment]::SetEnvironmentVariable("**OPENAI\_API\_KEY**", "SK-XXXXXX", "**User**")

OR

1. Set system-wide (Run cmd as Administrator)

[Environment]::SetEnvironmentVariable("OPENAI\_API\_KEY", "SK-XXXXXX", "**Machine**")

setx does **not** affect the current terminal session—open a new one.

1. Open New Powershell & Verfiy if set or not?

[Environment]::GetEnvironmentVariable("OPENAI\_API\_KEY", "User")

1. Remove the variable

[Environment]::SetEnvironmentVariable('OPENAI\_API\_KEY', $null, 'User')

**In Linux /Mac:**

export OPENAI\_API\_KEY="your\_api\_key\_here"

Example: Using OpenAI SDK (Python)

**Setup the Project:**

Open Terminal (cmd) and execute following commands

mkdir pythondemos

cd pythondemos

code . #Open VS Code

**Setup the Virtual Environment in Python**

Go to Terminal (Menu in VS Code) 🡪 New Terminal

python -m venv myenv **#Create a Virtual Environment**

myvenv\Scripts\activate (In Windows)

source myvenv/bin/activate (In Mac or Linux)

**Step1:** Install OpenAI API module

pip install openai

**demo.py (Chat Completion API)**

from openai import OpenAI

client = OpenAI()

completion = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=[

        {

            "role": "user",

            "content": "What is OpenAI"

        }

    ]

)

print(completion.choices[0].message.content)

print(completion.usage.prompt\_tokens, completion.usage.completion\_tokens, completion.usage.total\_tokens)

**demo.py (Response API)**

from openai import OpenAI

from dotenv import load\_dotenv

import os

load\_dotenv()

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

response = client.responses.create(

    model="gpt-5.6-luna",

    input="What is OpenAI",

)

print(response.output\_text)

print(f"Tokens used - Input: {response.usage.input\_tokens}, " f"Output: {response.usage.output\_tokens}")

**Benefits of Response API over Chat Completion API**

1. Better Perfomance
2. Agentic by default
3. Lower costs because of improved caching
4. Stateful context
5. Flexible input either as string or list of messages.
6. Future proof for uplcoming models

![](data:image/png;base64...)

**Responses-demo.py (Response API)**

from openai import OpenAI

client = OpenAI()

response = client.**responses**.create(

    model="gpt-5.6-luna",

    input="What is OpenAI",

**reasoning={"effort": "minimal"} OR medium/high,**

)

print(response.output\_text)

print(f"Tokens used - Input: {response.usage.input\_tokens}, " f"Output: {response.usage.**output\_tokens**}")

print(f"Reasoning tokens: {response.usage.output\_tokens\_details.**reasoning\_tokens**}")

Conversation and Context

While each text generation request is independent and stateless (unless you are using [assistants](https://platform.openai.com/docs/assistants/overview)), you can still implement **multi-turn conversations** by providing additional messages as parameters to your text generation request.

**The playground enables you to enter System message, user message and a set of *parameters* that control the completions returned by the model:**

**Message Categories**

1. **Developer / System message:** The system message is included at the beginning of the prompt and is used to prime the model and you can include a variety of information in the system message including:

* A brief description of the assistant
* The personality of the assistant
* Instructions for the assistant
* Data or information needed for the model

1. **User messages** contain instructions that request a particular type of output from the model. You can think of user messages as the messages you might type in to ChatGPT as an end user.
2. **Assistant message:** Response of AI for the User message and context in it.

**System / Developer and User messages:**

In the [chat completions](https://platform.openai.com/docs/api-reference/chat/) API, you create prompts by providing an **array of messages** that contain instructions for the model. Each message can have a different **role**, which influences how the model might interpret the input.

messages = [

    {

        "role": "developer",

        "content": "You are a Professor of ML named MLGuru who can answers ML questions for a 10 class student. Apart from ML related questions ignore all other questions"

    },

    {

        "role": "user",

        "content": "What is perfect definition of AI?",

    },

]

Note: A good thing to know is that there is one system message for the whole conversation.
When you are building applications, the system message is mostly not visible for your end user and added programiticly.

**Build the Conversation using Prompt and Completion**

**Conversation Context**

**====================**

System Message is msg[0]

User Message is msg[1]

Assistant Message is msg[2]

User Message is msg[3]

Assistant Message is msg[4]

User Message is msg[5]

Assistant Message is msg[6]

**Example:**

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

# Define the messages

messages = [

    {"role": "system", "content": "You are a professor of AI and can answer all questions related to AI and ML for students of class 10" },

    {"role": "user", "content": "What is OpenAI" }

]

completion = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=messages

)

# Print the response

print(completion.choices[0].message.content)

print(completion.usage.completion\_tokens)

print(completion.usage.total\_tokens)

messages.append({"role": "assistant", "content": completion.choices[0].message.content})

messages.append({"role": "user", "content": "What are its benefits"})

completion = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=messages

)

print("="\*50, "Benefits", "="\*50)

print(completion.choices[0].message.content)

print(completion.usage.completion\_tokens)

print(completion.usage.total\_tokens)

messages.append({"role": "assistant", "content": completion.choices[0].message.content})

messages.append({"role": "user", "content": "Explain more in detailed about the first benefit"})

completion = **client.chat.completions.create**(

    model="gpt-5.6-luna",

    messages=messages

)

print("="\*50, "Benefits", "="\*50)

print(completion.choices[0].message.content)

print(completion.usage.completion\_tokens)

print(completion.usage.total\_tokens)

**Using Loop: (Chat Completion API)**

# Define the messages

from openai import OpenAI

client = OpenAI()

# Define the messages

messages = [

    {"role": "developer", "content": "You are an expert in AI and ML Subject. You can answer any question about AI and ML at an entry level learners. You must regret to answer questions not related to AI and ML" },

]

while True:

    user\_input = input("You: ")

    if user\_input.lower() == "exit":

        break

    messages.append( {"role": "user", "content": user\_input })

    completion = client.chat.completions.create(

        model="gpt-5.6-luna",

        messages=messages,

    )

    # Print the response

    print(completion.choices[0].message.content)

    print ("\*"\*20, completion.usage.prompt\_tokens, "\*"\*20, completion.usage.completion\_tokens, "\*"\*20, completion.usage.total\_tokens, "\*"\*20)

#messages.append( {"role": "assistant", "content": completion.choices[0].message.content} )

**messages.append**(completion.choices[0].message)

**Using Loop (response API)**

# Define the messages

from openai import OpenAI

client = OpenAI()

# Define the messages

Developer\_message = {

"role": "developer",

"content": "You are an expert in AI and ML Subject. You can answer any question about AI and ML at an entry level learners. You must regret to answer questions not related to AI and ML"

}

response = None

while True:

    user\_input = input("You: ")

    if user\_input.lower() == "exit":

        break

if response is None:

current\_input = [developer\_message, {"role": "user", "content": user\_input}]

else:

current\_input = [{"role": "user", "content": user\_input}]

    response = client.responses.create(

        model="gpt-5.6-luna",

        input=current\_input,

**previous\_response\_id**=response.id if response else None  # Set to None for a new conversation

    )

    # Print the response

    reply = response.output\_text

    print(reply)

    if hasattr(response, "usage"):

        print("\*" \* 20, response.usage.input\_tokens, "\*" \* 20, response.usage.output\_tokens, "\*" \* 20, response.usage.total\_tokens, "\*" \* 20,

        )

    #messages.append( {"role": "assistant", "content": reply} ) – Commented because we have used previous\_response\_id

By using alternating user and assistant messages, you can capture the previous state of a conversation in one request to the model.

**Note:**

* As your inputs become more complex, or you include more and more turns in a conversation, you will need to consider both **output token** and **context window** limits.
* If you create a very large prompt (usually by including a lot of conversation context or additional data/examples for the model), you run the risk of exceeding the allocated context window for a model, which might result in truncated outputs.