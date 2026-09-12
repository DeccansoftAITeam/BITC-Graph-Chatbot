Controlling LLM Behavior using Request Parameters

1. **max\_tokens / max\_output\_tokens:** Set a limit on the number of output tokens per model response. Setting too low may truncate responses.
2. **Temperature**: Controls randomness. Typically ranges from 0 to infinity, though values between 0 and 2 are most common.
   * **Lower values (e.g., 0.0 - 0.3)**: The model generates more **deterministic** and **predictable** responses.
     + **The context is "The cat sat on a \_\_\_"**
     + Probabilities remain unchanged: **mat**: 0.50, **couch**: 0.20, **floor**: 0.15, **table**: 0.10, **window**: 0.05
     + Higher probabilities become even higher, and lower probabilities become even lower. For example: mat: 0.70, couch: 0.15, floor: 0.10, table: 0.04, window: 0.01
     + The model becomes more confident and deterministic, making **"mat"** much more likely.
   * **Medium values (e.g., 0.5 - 0.7)**: The model balances **coherence and creativity**.
     + **The model is likely to choose** "mat" **but could pick others with some other probability.**
   * **Higher values (e.g., 1.0 - 2.0)**: The model becomes more **creative and random**, potentially introducing unexpected or imaginative outputs.
   * Probabilities are spread more evenly: mat: 0.40, couch: 0.25, floor: 0.20, table: 0.10, window: 0.05

**Now, the model is more willing to explore less probable options like** "couch" **or** "floor"**.**

Best Use Cases for Different Temperature Values

|  |  |
| --- | --- |
| **Temperature** | **Best Use Case** |
| 0.0 - 0.3 | Focused and deterministic. Fact-based tasks, coding, precise answers, structured responses. |
| 0.4 - 0.7 | Balanced. Conversational AI, storytelling, content writing with coherence. |
| 0.8-1.2 | Poetry, and imaginative scenarios. |
| 1.2 - 2.0 | Very random, Extremely Creative (story writing, brainstorming) |

**Example:**

def example\_chat\_temperature():

prompt = "Write a tagline for a tech startup"

***# Low temperature - focused***

response\_low = client.chat.completions.create(

model="gpt-5.6-luna",

messages=[{"role": "user", "content": prompt}],

**temperature=0.2**

)

print(f"Low temp (0.2): {response\_low.choices[0].message.content}")

***# High temperature - creative***

response\_high = client.chat.completions.create(

model="gpt-5.6-luna",

messages=[{"role": "user", "content": prompt}],

**temperature=1.5**

)

print(f"High temp (1.5): {response\_high.choices[0].message.content}")

1. **Top-p (Nucleus Sampling):** parameter controls how the model selects words when generating responses. It determines the probability mass from which tokens are drawn.

How it works:

* The model calculates the cumulative probability of all tokens.
* It sorts tokens by probability and chooses only from the smallest set of tokens that sum to p or more.
* Once the subset is determined, the next token is sampled from this subset.

Values:

* 0.1: Only top 10% probability tokens
* 0.5: Top 50% probability tokens
* 1.0: All tokens considered (default)

Note: Try adjusting temperature or Top P but not both.

**Example of Top P**

Imagine a language model is generating the next word in the sentence:
*"The cat sat on the..."*

The model predicts probabilities for the next possible words:

|  |  |
| --- | --- |
| **Word** | **Probability** |
| mat | 0.50 |
| couch | 0.20 |
| floor | 0.15 |
| table | 0.10 |
| window | 0.05 |

**Top-p chooses from a dynamic subset of words, ensuring the selected options account for a cumulative probability of at least p.**

**Here’s how it works:**

* Top-p = 0.9**:**
  + The model considers only the smallest set of words whose probabilities sum to 0.9:
    - mat (0.50) + couch (0.20) + floor (0.15) = 0.85
    - Add **"table" (0.10)** → cumulative = 0.95
    - So, the set becomes: mat, couch, floor, table

"window" **is excluded because it contributes only 0.05 and is outside the 0.9 threshold.**

* Top-p = 0.7**:**
  + The model selects the smallest set of words whose probabilities sum to 0.7:
    - mat (0.50) + couch (0.20) = 0.70
    - The set becomes: mat, couch

"floor," "table," and "window" **are excluded as their cumulative probabilities exceed 0.7.**

* Top-p = 0.3**:**
  + The model selects the smallest set of words whose probabilities sum to 0.7:
    - mat (0.50)
    - The set becomes: only mat

**Let’s combine** Temperature **and** Top-p**:**

|  |  |
| --- | --- |
| **Setting** | **Effect** |
| High temp + high top-p | Very creative, sometimes chaotic |
| Low temp + low top-p | Extremely rigid, repetitive |
| High temp + low top-p | Controlled creativity |
| Low temp + high top-p | Mostly deterministic, but safe (Factual / reasoning / coding) |

**Strong Recommendation: Use either Temperature or Top-p**

1. **Stop** **sequences**: Make responses stop at a desired point, such as the end of a sentence or list.
   * Specify up to four sequences where the model will stop generating further tokens in a response.
   * The returned text won't contain the stop sequence.
   * **Practical Use**: Useful f or chatbots, structured responses, code generation, and controlled text outputs.
   * **Caution**: If a stop sequence **isn’t** encountered in the generated text, the model continues generating until the maximum token limit is reached.
   * Always ensure the stop sequence is likely to appear in the context of your prompt.

response = client.chat.completions.create(

model="gpt-5.6-luna",

messages=[{"role": "user", "content": "List programming languages:\n1."}],

**stop=["\n5, "\n\n"], # Stop after listing 4 items**

max\_tokens=200

)

print(response.choices[0].message.content)

1. **Frequency** **penalty and Presense penalty**: This penalty reduces the likelihood of a token being repeated based on how many times it has already appeared. Not applicable to reasoning models.

* **frequency\_penalty** = *“stop saying it again and again”*
* **presence\_penalty** = *“you’ve mentioned it once, move on”*

**Example:** If a generated passage already contains the word "innovation" three times, applying a frequency penalty will make it less likely for "innovation" to appear a fourth time.

|  |  |
| --- | --- |
| **Penalty Value** | **Best Use Case** |
| -1.0 to -2.0 | Encourages repetition (useful in poetry, mantras, slogans) |
| 0.0 (default) | Normal responses, the model naturally decides word choice. (Code Generation) |
| 0.5 - 1.0 | Balanced responses, avoiding excessive repetition (Long explanations / essays) |
| 1.5 - 2.0 | Forces the model to use synonyms & rephrase sentences |

**Example**:
Prompt: *"The cat is"*
= -1.0: *"The* ***cat*** *is sleeping on the mat. The* ***cat*** *is happy. The* ***cat*** *is hungry."*
= 1.0: *"The* ***cat*** *is sleeping on the mat. It looks happy and hungry."*

Storing the Response on OpenAI Server

* If store=True (for response API), OpenAI **stores the generated response along with its response.id**.
* You can later **retrieve this response by using its ID** with the **client.responses.retrieve()** method.
* This is useful when you want to **maintain a record of conversations, audit logs, or retrieve responses without regenerating them**.
* Set to **false** for privacy-sensitive applications

from openai import OpenAI

client = OpenAI()

messages = [

    {"role": "user", "content": "Tell me a joke about programmers."}

]

# Create and store the response

response = client.responses.create(

    model="o4-mini",

    input=messages,

    store=True  # Store the response for later retrieval

)

print("Response ID:", **response.id**)

print("Generated Output:", response.output\_text)

# Later in another part of the program, retrieve the response:

retrieved = client.responses.retrieve(**response.id**)

print("Retrieved Output:", retrieved.output\_text)

Metadata

metadata is developer-defined key–value information that travels with the request or response, but does NOT affect model output.

Use cases:

* User tracking
* Request source identification
* A/B testing
* Analytics

***Example***

def example\_responses\_metadata():

response = client.responses.create(

model="gpt-5.6-luna",

input="Explain RESTful APIs",

**metadata**={

"user\_id": "user\_12345",

"session\_id": "session\_abc",

"feature": "tutorial\_chatbot",

"version": "v1.2.0"

}

)

print(f"Response ID: {response.id}")

print(response.output\_text)

Background Mode

Agents like [Codex](https://openai.com/index/introducing-codex/) and [Deep Research](https://openai.com/index/introducing-deep-research/) show that reasoning models can take several minutes to solve complex problems. Background mode enables you to execute long-running tasks on models like GPT-5.6-LUNA and GPT-5.6-LUNA pro reliably, without having to worry about timeouts or other connectivity issues.

Background mode kicks off these tasks asynchronously, and developers can poll response objects to check status over time. To start response generation in the background, make an API request with background set to true:

from openai import OpenAI

from time import sleep

client = OpenAI()

resp = client.responses.create(

model="gpt-5.6-luna",

input="Write a very long novel about otters in space.",

background=True,

)

**# Start Poling for status:**

while resp.status in {"queued", "in\_progress"}:

print(f"Current status: {resp.status}")

sleep(2)

resp = **client.responses.retrieve**(resp.id)

print(f"Final status: {resp.status}\nOutput:\n{resp.output\_text}")

Cancelling a background response

resp = **client.responses.cancel**("resp\_123")

Streaming API Responses

HTTP response. When generating long outputs, waiting for a response can take time. Streaming responses lets you start printing or processing the beginning of the model's output while it continues generating the full response.

**Response API:**

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

# Start streaming response using Responses API

stream = client.responses.create(

    model="gpt-5.6-luna",

    input=[

        {"role": "user", "content": "Create a poem about the beauty of nature"}

    ],

    stream=True,

)

for chunk in stream:

    if chunk.type == "response.**output\_text.delta**":  # Partial text output

        print(chunk.delta, end="", flush=True)

    elif chunk.type == "response.completed":  # Completed response

        print("\n\n--- Response Completed ---")

Webhooks

OpenAI webhooks allow you to receive real-time notifications about events in the API, such as when a batch completes, a background response is generated, or a fine-tuning job finishes.

Webhooks are configured per-project.

To start receiving webhook requests on your server, log in to the dashboard and [open the webhook settings page](https://platform.openai.com/settings/project/webhooks).

![webhook endpoint edit dialog](data:image/png;base64...)

After creating a new webhook, you'll receive a signing secret to use for server-side verification of incoming webhook requests. Save this value for later, since you won't be able to view it again.

With your webhook endpoint created, you'll next set up a server-side endpoint to handle those incoming event payloads.

When an event happens that you're subscribed to, your webhook URL will receive an HTTP POST request like this:

POST https://yourserver.com/webhook

user-agent: OpenAI/1.0 (+https://platform.openai.com/docs/webhooks)

content-type: application/json

webhook-id: wh\_685342e6c53c8190a1be43f081506c52

webhook-timestamp: 1750287078

webhook-signature: v1,K5oZfzN95Z9UVu1EsfQmfVNQhnkZ2pj9o9NDN/H/pI4=

{

"object": "event",

"id": "evt\_685343a1381c819085d44c354e1b330e",

"type": "response.completed",

"created\_at": 1750287018,

"data": { "id": "resp\_abc123" }

}

**Verifying webhook signatures:**

When you create a webhook endpoint in the OpenAI dashboard, you'll be given a signing secret that you should make available on your server as an environment variable:

export OPENAI\_WEBHOOK\_SECRET="<your secret here>"

The simplest way to verify webhook signatures is by using the unwrap() method of the official OpenAI SDK helpers:

Signature verification with the OpenAI SDK

client = OpenAI()

webhook\_secret = os.environ["OPENAI\_WEBHOOK\_SECRET"]

**@app.post("/openai/webhook")**

async def openai\_webhook(request: Request):

try:

# Raw request body (bytes)

body = await request.body()

# Verify + parse event

event = **client.webhooks.unwrap**(

body,

request.headers,

secret=**webhook\_secret**

)

except Exception as e:

# Signature invalid or malformed payload

raise HTTPException(status\_code=400, detail=str(e))

Prompt Caching

* **Prompt caching** means **reusing the already-processed part of a prompt** so the model doesn’t re-read and re-process the same tokens again and again.
* If the starting part of the prompt is identical, caching is used automatically.
* Structure prompts with **static or repeated content at the beginning** and dynamic, user-specific content at the end.
* Caching is enabled automatically for prompts that are 1024 tokens or longer.
* You do not enable it.
* Put static content (system prompt) at the beginning, variable content (user message) at the end
* Caches are typically cleared after 5-10 minutes of inactivity

**When You SHOULD Use Prompt Caching**

✔️ Agent-based systems
✔️ Chat apps with fixed system roles
✔️ Internal tools with heavy instructions
✔️ Evaluation / moderation pipelines

Example: Same prefix → automatic prompt caching.

from openai import OpenAI

client = OpenAI(

    api\_key="sk-proj-\_LblgOJoA"

)

SYSTEM\_PROMPT = """

You are a senior backend architect.

Follow clean architecture principles.

Return output in JSON only.

Use PostgreSQL best practices.

"""

SYSTEM\_PROMPT = **SYSTEM\_PROMPT \* 50**

def call\_llm(user\_input):

    response = client.chat.completions.create(

        model="gpt-5.6-luna",

        messages=[

            {"role": "system", "content": SYSTEM\_PROMPT},

            {"role": "user", "content": user\_input},

        ]

    )

    usage = response.usage

    print("Prompt tokens:", usage.prompt\_tokens)

    # Safe access to cached tokens

    cached\_tokens = 0

    if hasattr(usage, 'prompt\_tokens\_details') and usage.prompt\_tokens\_details:

        cached\_tokens = getattr(usage.prompt\_tokens\_details, 'cached\_tokens', 0)

    print("Cached tokens:", cached\_tokens)

    print("Output tokens:", usage.completion\_tokens)

    print("Total tokens:", usage.total\_tokens)

    print("-" \* 40)

    return response.choices[0].message.content

# Multiple calls with same system prompt

call\_llm("Design a user table schema")

call\_llm("Add indexes for the same table")

call\_llm("Suggest partitioning strategy")

**What can be cached**

* **Messages:** The complete messages array, encompassing system, user, and assistant interactions.
* **Images:** Images included in user messages, either as links or as base64-encoded data, as well as multiple images can be sent. Ensure the detail parameter is set identically, as it impacts image tokenization.
* **Tool use:** Both the messages array and the list of available tools can be cached, contributing to the minimum 1024 token requirement.
* **Structured outputs:** The structured output schema serves as a prefix to the system message and can be cached.

Reasoning Model

**Reasoning models** generate an internal chain of thought to analyze the input prompt, and excel at understanding complex tasks and multi-step planning. They are also generally slower and more expensive to use than GPT models.

OpenAI provide smaller, faster models (gpt-5.6-luna) that are less expensive per token. The larger model (gpt-5.6-sol) is slower and more expensive but often generates better responses for complex tasks and broad domains.

**How reasoning works**

Reasoning models introduce **reasoning tokens** in addition to input and output tokens. The models use these reasoning tokens to "**think**," breaking down the prompt and considering multiple approaches to generating a response. After generating reasoning tokens, the model produces an answer as visible completion tokens and discards the reasoning tokens from its context.

Note: While reasoning tokens are not visible via the API, they still occupy space in the model's context window and are billed as output tokens.

The exact number of reasoning tokens used is visible in the [usage object of the response object](https://platform.openai.com/docs/api-reference/responses/object), under output\_tokens\_details.

{

"usage": {

"input\_tokens": 75,

"input\_tokens\_details": {

"cached\_tokens": 0

},

"output\_tokens": 1186,

"output\_tokens\_details": {

**"reasoning\_tokens": 1024**

},

"total\_tokens": 1261

}

}

**Why OpenAI does not expose chain-of-thought**

This is a deliberate policy decision due to:

* Safety and misuse concerns
* Preventing reverse-engineering
* Ensuring consistent, aligned behavior
* Avoiding leakage of internal model mechanics

Reasoning summary output is part of the summary array in the reasoning [output item](https://platform.openai.com/docs/api-reference/responses/object#responses/object-output). This output will not be included unless you explicitly opt in to including reasoning summaries.

from openai import OpenAI

client = OpenAI()

response = client.responses.create(

model="gpt-5.6-luna",

input="What is the capital of France?",

reasoning={

"effort": "low",

"summary": "auto"

}

)

print(response.output)