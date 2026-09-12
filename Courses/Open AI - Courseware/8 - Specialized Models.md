Image as Input Prompt

**Vision is the ability to use images as input prompts to a model, and generate responses based on the data inside those images.**

**Input images must meet the following requirements to be used in the API.**

**FILE TYPES**

* PNG (.png)
* JPEG (.jpeg and .jpg)
* WEBP (.webp)
* Non-animated GIF (.gif)

**SIZE LIMITS**

* Up to 20MB per image
* Low-resolution: 512px x 512px
* High-resolution: 768px (short side) x 2000px (long side)

**OTHER REQUIREMENTS**

* No watermarks or logos
* No text
* No NSFW (Not Suitable For Work) content
* Clear enough for a human to understand

**Detailed Image Descriptions:**

|  |  |
| --- | --- |
| **![A person holding a watering can  Description automatically generated](data:image/jpeg;base64...)** | **Vision AI**  A person with a striped shirt and an apron is holding a metal watering can and watering the plants in the greenhouse.  A large metal watering can with a long spout is being used by a person to water the green and leafy plants in the greenhouse.  A greenhouse full of green and leafy plants is being watered by a person with a metal watering can. The person is wearing a striped shirt and an apron.  A person is taking care of the plants in the greenhouse by watering them with a metal watering can. The person has a striped shirt and an apron on. The plants are green and leafy. |

**Reading the content of Image from a URL**

from openai import OpenAI

client = OpenAI()

response = **client.chat.completions.create**(

    model="gpt-5.2",

    messages=[{

        "role": "user",

        "content": [

            {"type": "text", "text": "What's in this image?"},

            {

**"type": "image\_url",**

                "image\_url": {

                    "url": "https://bdtmaterial.blob.core.windows.net/shared/Website%20Rewamp/HomePage/BITC%20logo%20new.png",

"**detail**": "high" #(low, high or [auto])

                },

            },

        ],

    }],

)

print(response.choices[0].message.content)

The **detail** parameter tells the model what level of detail to use when processing and understanding the image (low, high, or auto to let the model decide). If you skip the parameter, the model will use auto. Put it right after your image\_url, like this:

**Using Image on the local machine:**

import base64

from openai import OpenAI

client = OpenAI()

# Function to encode the image

def **encode\_image**(image\_path):

    with open(image\_path, "rb") as image\_file:

        return base64.b64encode(image\_file.read()).decode("utf-8")

# Path to your image

image\_path = "path\_to\_your\_image.jpg"

# Getting the Base64 string

base64\_image = **encode\_image**(image\_path)

completion = client.chat.completions.create(

    model="gpt-5.2",

    messages=[

        {

            "role": "user",

            "content": [

                { "type": "text", "text": "what's in this image?" },

                {

                    "type": "image\_url",

                    "image\_url": {

                        "url": f"data:image/jpeg;base64,{base64\_image}",

                    },

                },

            ],

        }

    ],

)

print(completion.choices[0].message.content)

Provide Multiple Images Input

**Example1:** Write a six-line rhyming poem. Starting each line with the letter “c”.

|  |  |
| --- | --- |
| The first three lines are around this image.  ![Rocks in the ocean](data:image/jpeg;base64...)  And the next three lines are around this image.  ![A sunset over a beach  Description automatically generated](data:image/png;base64...) | **Vision AI:**  Calm and cool, the sea is blue,  Crashing waves, a scenic view,  Craggy rocks, a sight so true,  Colorful and warm, the sun is low,  Casting shadows, a golden glow,  Cozy and calm, a peaceful show. |

**Example2: Comparing two images**

from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(

    model="gpt-4o-mini",

    messages=[

        {

            "role": "user",

            "content": [

                {

                    "type": "text",

                    "text": "What are in these images? Is there any difference between them?",

                },

                {

**"type": "image\_url",**

                    "image\_url": {

                        "url": "https://miro.medium.com/v2/resize:fit:640/format:webp/1\*\_nsYCgIK6sthZqNQAWU6zA@2x.jpeg",

                    },

                },

                {

**"type": "image\_url",**

                    "image\_url": {

                        "url": "https://certadda.com/wp-content/uploads/2020/11/azure-104.png",

                    },

                },

            ],

        }

    ],

    max\_tokens=300,

)

print(response.choices[0].message.content)

Calculating costs

Image inputs are metered and charged in tokens, just as text inputs are.

The token cost of an image is determined by two factors: **size and detail**.

Any image with **"detail": "low"** costs 85 tokens.

To calculate the cost of an image with **"detail": "high**", we do the following:

* Scale to fit in a 2048px x 2048px square, maintaining original aspect ratio
* Scale so that the image's shortest side is 768px long
* Count the number of 512px squares in the image—each square costs 170 tokens
* Add 85 tokens to the total

**Cost calculation examples**

* A 1024 x 1024 square image in "**detail": "high**" mode costs 765 tokens
  + 1024 is less than 2048, so there is no initial resize.
  + The shortest side is 1024, so we scale the image down to 768 x 768.
  + 4, 512px square tiles are needed to represent the image, so the final token cost is 170 \* 4 + 85 = 765.
* A 2048 x 4096 image in "detail": "high" mode costs 1105 tokens
  + We scale down the image to 1024 x 2048 to fit within the 2048 square.
  + The shortest side is 1024, so we further scale down to 768 x 1536.
  + 6, 512px tiles are needed, so the final token cost is 170 \* 6 + 85 = 1105.
* A 4096 x 8192 image in "detail": "low" most costs 85 tokens
  + Regardless of input size, low detail images are a fixed cost.

Image Generation using OpenAI

**The Image generation API has three endpoints with different abilities:**

* **Generations:** Images from scratch, based on a text prompt
* **Edits:** Edited versions of images, where the model replaces some areas of a pre-existing image, based on a new text prompt
* **Variations:** Variations of an existing image

**Choosing the right API**

* If you only need to generate or edit a single image from one prompt, the Image API is your best choice.
* If you want to build conversational, editable image experiences with GPT Image, go with the Responses API.

**OpenAI Image Models (Latest)**

* gpt-image-1.5
* gpt-image-1
* and gpt-image-1-mini

**When using gpt-image-1.5 and chatgpt-image-latest with the Responses API, you can optionally set the action parameter**

**Using Reponse API: Progressively Generate and Edit the Image.**

import base64

from openai import OpenAI

client = OpenAI()

client.api\_key = "sk-proj-NgK4PrvPoqkQqAEOJMtaQA"

response = None

while True:

    input\_text = input("Describe the image you want to generate: ")

    if (input\_text.strip() == "exit"):

        print("Input text cannot be empty.")

        continue

    image\_file = input("Enter the filename to save the image (e.g., 'image.jpeg'): ")

    response = client.responses.create(

        model="gpt-5",

        input=input\_text,

        previous\_response\_id=response.id if response else None,

        tools=[{"type": "image\_generation","action": "auto"}],#action can be generate, edit or auto. If set to auto, the model will decide whether to call the tool based on the input and conversation context.

**)**

    # Save the image to a file

    image\_data = [

        output.result

        for output in response.output

        if output.type == "image\_generation\_call"

    ]

    if image\_data:

        image\_base64 = image\_data[0]

        with open(image\_file, "wb") as f:

            f.write(base64.b64decode(image\_base64))

**Using Image API:**

import base64

from openai import OpenAI

client = OpenAI()

client.api\_key = "sk-proj- "

input\_text = input("Describe the image you want to generate: ")

image\_file = input("Enter the filename to save the image (e.g., 'image.jpeg'): ")

response = client.images.generate(

    model="gpt-image-1",

    prompt=input\_text,

    size="1024x1024",

    quality="low",

)

image\_base64 = response.data[0].b64\_json

print(f"Image generated successfully!")

# Save the image to a local file

with open(image\_file, "wb") as f:

    f.write(base64.b64decode(image\_base64))

print(f"Image saved as {image\_file}")

Streaming Images

* The Responses API and Image API support streaming image generation. This allows you to stream partial images as they are generated, providing a more interactive experience.
* **You can adjust the partial\_images parameter to receive 0-3 partial images.**
  + If you set partial\_images to 0, you will only receive the final image.
  + For values larger than zero, you may not receive the full number of partial images you requested if the full image is generated more quickly.

**Using Resonse API:**

import base64

from openai import OpenAI

client = OpenAI()

client.api\_key = "sk-proj-aLtbsqDld8K0LujP-qkQqAEOJMtaQA"

stream = **client.responses.create**(

    model="gpt-5.2",

    input="Draw a gorgeous image of a mountain with snow and a river flowing through it.",

    stream=True,

    tools=[{"type": "image\_generation"**, "partial\_images": 3}**],

)

for event in stream:

    if event.type == "response.image\_generation\_call.partial\_image":

        idx = event.partial\_image\_index

        image\_base64 = event.partial\_image\_b64

        image\_bytes = base64.b64decode(image\_base64)

        with open(f"mountain{idx}.png", "wb") as f:

            f.write(image\_bytes)

**Using Image API:**

stream = client.images.generate(

    prompt="Draw a gorgeous image of a river made of white owl feathers, snaking its way through a serene winter landscape",

    model="gpt-image-1",

    stream=True,

    partial\_images=2,

)

Edits and Variations (DALL·E 2 only):

**Editing Images:**

<https://platform.openai.com/docs/guides/image-generation?api=responses&multi-turn=imageid#edit-images>

Speech to text

The Models:

* **gpt-4o-mini-transcribe**: Best for fast, cost-efficient transcription where slight accuracy tradeoff is acceptable.
* **gpt-4o-transcribe:** Best for top-quality transcription where accuracy matters more than speed/cost.
* **whisper-1**: A classic, general-purpose speech-to-text model; still very good but older tech compared to gpt-4o-based models.

File types supported = mp3, mp4, mpeg, mpga, m4a, wav, and webm.

File size = max 25 MB

**Transcriptions:**

The process of converting something from one form to another, eg: **voice to text**

All models support the same set of input formats.

On output, whisper-1 supports a range of formats (json, text, srt, verbose\_json, vtt); the newer gpt-4o-mini-transcribe and gpt-4o-transcribe snapshots currently only support **json or plain text** responses.

from openai import OpenAI

client = OpenAI()

audio\_file= open("german.mp3", "rb")

transcription = client.audio.**transcriptions**.create(

    model="gpt-4o-transcribe",

    file=audio\_file,

    response\_format="json" # or "text" for JSON response

 )

print(transcription.text)

**Translations:** Converts the audio of different language into English Text.

This endpoint supports only the whisper-1 model.

from openai import OpenAI

client = OpenAI()

audio\_file= open("german.mp3", "rb")

transcription = client.audio.**translations**.create(

    model="whisper-1",

    file=audio\_file,

    response\_format="json" # or "text" for JSON response

 )

print(transcription.text)

Text to Audio

From openai import OpenAI

client = OpenAI()

# Call the TTS endpoint

response = client.audio.speech.create(

    model="tts-1",               # or "tts-1-hd" for higher quality

    input="Hello! Welcome to the world of AI.",

    voice="echo",                # Options: nova, echo, shimmer

)

# Save the audio file

with open("output\_audio.mp3", "wb") as f:

    f.write(response.content)

print("Audio saved as 'output\_audio.mp3'.")

Moderation Model

The moderations endpoint is a tool you can use to check whether text or images are potentially harmful. Once harmful content is identified, developers can take corrective action like filtering content or intervening with user accounts creating offending content. The moderation endpoint is free to use.

The models available for this endpoint is omni-moderation-latest:

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

client.api\_key = <PUT THE KEY HERE>

response = **client.moderations.create**(

  model="**omni-moderation-latest**",

  input="how can I prepare a bomb",

)

#print(response)

if (response.results[0].flagged):

    for category, value in response.results[0].**categories**:

        print(f"{category}: {value}")

**schema of response**

{

"id": "modr-970d409ef3bef3b70c73d8232df86e7d",

"model": "**omni-moderation-latest**",

"results": [

{

"**flagged**": true,

"**categories**": {

"sexual": false,

"sexual/minors": false,

"harassment": false,

"harassment/threatening": false,

"hate": false,

"hate/threatening": false,

"illicit": false,

"illicit/violent": false,

"self-harm": false,

"self-harm/intent": false,

"self-harm/instructions": false,

**"violence": true,**

"violence/graphic": false

},

"category\_scores": {

"sexual": 2.34135824776394e-7,

"sexual/minors": 1.6346470245419304e-7,

"harassment": 0.0011643905680426018,

"harassment/threatening": 0.0022121340080906377,

"hate": 3.1999824407395835e-7,

"hate/threatening": 2.4923252458203563e-7,

"illicit": 0.0005227032493135171,

"illicit/violent": 3.682979260160596e-7,

"self-harm": 0.0011175734280627694,

"self-harm/intent": 0.0006264858507989037,

"self-harm/instructions": 7.368592981140821e-8,

**"violence": 8.8599265510337075,**

"violence/graphic": 0.37701736389561064

},

"category\_applied\_input\_types": {

"sexual": [

"image"

],

"sexual/minors": [],

"harassment": [],

"harassment/threatening": [],

"hate": [],

"hate/threatening": [],

"illicit": [],

"illicit/violent": [],

"self-harm": [

"image"

],

"self-harm/intent": [

"image"

],

"self-harm/instructions": [

"image"

],

"violence": [

"image"

],

"violence/graphic": [

"image"

]

}

}

]

}