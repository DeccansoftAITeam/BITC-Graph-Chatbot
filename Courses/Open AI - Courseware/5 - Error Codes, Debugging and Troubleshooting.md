Error Codes

Python Library Error Types

|  |  |
| --- | --- |
| **Type** | **Overview** |
| APIConnectionError | Issue connecting to our services. |
| APITimeoutError | Request timed out. |
| AuthenticationError | Your API key or token was invalid, expired, or revoked. |
| BadRequestError | Your request was malformed or missing some required parameters, such as a token or an input. |
| ConflictError | The resource was updated by another request. |
| InternalServerError | Issue on our side. |
| NotFoundError | Requested resource does not exist. |
| PermissionDeniedError | You don't have access to the requested resource. |
| RateLimitError | You have hit your assigned rate limit. |
| UnprocessableEntityError | Unable to process the request despite the format being correct. |

from openai import OpenAI, **APIError, APIConnectionError, RateLimitError**

import os

from dotenv import load\_dotenv

load\_dotenv()

try:

    messages = [

        {

            "role": "user",

            "content": "What is OpenAI"

        }

    ]

    client = OpenAI()

    response = client.chat.completions.create(

        messages=messages,

        model="gpt-5.6-nano"

    )

except **APIConnectionError** as e:

    # Handle connection error here

    print(f"Failed to connect to OpenAI API: {e}")

    pass

except **RateLimitError** as e:

    # Handle rate limit error (we recommend using exponential backoff)

    print(f"OpenAI API request exceeded rate limit: {e}")

    pass

except **APIError** as e:

    # Handle API error here, e.g. retry or log

    print(f"OpenAI API returned an API Error: {e}")

    pass

**Error Codes Reference:**

<https://platform.openai.com/docs/guides/error-codes#python-library-error-types>

Debugging and Troubleshooting

In addition to error codes returned from API responses, it may sometimes be necessary to inspect HTTP response headers as well.

**API meta information**

* **openai-organization**: The [organization](https://platform.openai.com/docs/guides/production-best-practices#setting-up-your-organization) associated with the request
* **openai-processing-ms**: Time taken processing your API request
* **openai-version**: REST API version used for this request (currently 2020-10-01)
* **x-request-id**: Unique identifier for this API request (used in troubleshooting)

**OpenAI recommends logging request IDs in production deployments**, which will allow more efficient troubleshooting with our [support team](https://help.openai.com/en/) should the need arise

print(ex**.request\_id**)

**Rate limiting information**

* x-ratelimit-limit-requests
* x-ratelimit-limit-tokens
* x-ratelimit-remaining-requests
* x-ratelimit-remaining-tokens
* x-ratelimit-reset-requests
* x-ratelimit-reset-tokens

**Python code for accessing the raw response object**

from openai import OpenAI

import os

from dotenv import load\_dotenv

load\_dotenv()

client = OpenAI()

messages = [

    {

        "role": "user",

        "content": "What is OpenAI",

    },

]

# Make your OpenAI API request here

response = **client.chat.completions.with\_raw\_response.create**(

    messages=messages,

    model="gpt-4o-mini"

)

completion = response.parse()

print(completion.choices[0].message.content)

for header in response.headers:

    print(f"{header}: {response.headers[header]}")

print(response.headers.get(**'x-ratelimit-limit-tokens'**))