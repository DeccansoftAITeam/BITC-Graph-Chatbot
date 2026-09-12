Batch API with OpenAI

* A Batch API allows clients to send **multiple requests** in a single HTTP call. This reduces overhead and network latency compared to making separate calls for every request.
* The Batch API returns completions within 24 hours for a **50% discount**. <https://openai.com/api/pricing/>
* The service is ideal for processing jobs that **don't require immediate** responses.
* The API typically expects the batch **request** to be formatted in a certain way, such as a JSON object containing an **array of individual requests**. Each request in the array might include details like the HTTP method, endpoint, headers, and body.
* Likewise, the **response** usually consists of an **array of responses**, each corresponding to an individual request. The sequence of responses should match the order of requests unless the API supports asynchronous processing with varied ids or status.
* While some uses of the OpenAI Platform require you to send synchronous requests, there are many cases where requests do not need an immediate response or rate limits prevent you from executing a large number of queries quickly.

**Benefits of using BatchAI with OpenAI:**

* **Scalability:** Process large datasets quickly by distributing tasks across multiple computing nodes.
* **Efficiency:** Optimize resource utilization by parallelizing computations.
* **Cost-Effectiveness:** Reduce processing time and associated costs by leveraging cloud-based computing power.

**The Batch API offers a straightforward set of endpoints that allow you**

1. To collect a set of requests into a single file
2. Kick off a batch processing job to execute these requests
3. Query for the status of that batch while the underlying requests execute
4. Eventually retrieve the collected results when the batch is complete

**Available Endpoints in batch:**

1. /v1/completions  (Legacy)
2. /v1/chat/completions
3. /v1/responses
4. /v1/embeddings

Example

Batches start with a .jsonl file where each line contains the details of an individual request to the API.

**batch\_input.jsonl**

{"custom\_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1", "messages": [{"role": "system", "content": "You are a helpful assistant."},{"role": "user", "content": "Hello world!"}],"max\_tokens": 1000}}

{"custom\_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4.1", "messages": [{"role": "system", "content": "You are an unhelpful assistant."},{"role": "user", "content": "Hello world!"}],"max\_tokens": 1000}}

Note: The API typically expects a **single endpoint per batch job**

**#Prepare and upload your batch file**

batch\_input\_file = **client.files.create**(

    file=open("batch\_input.jsonl", "rb"),

    purpose="batch"

)

print(batch\_input\_file)

**#Creating the Batch**

batch\_input\_file\_id = batch\_input\_file.**id**

batch = **client.batches.create**(

    input\_file\_id=**batch\_input\_file\_id**,

    endpoint="/v1/chat/completions",

    completion\_window="24h",

    metadata={

        "description": "nightly eval job"

    }

)

print("Total: ", batch.request\_counts.total)

print("Completed: ", batch.request\_counts.completed)

print("Failed: ",batch.request\_counts.failed)

**#Listing existing batch Ids and status**

batches = **client.batches.list**(limit=10)

for batch in batches.data:

    print("Id=", **batch.id**, " Status=", **batch.status** )

The status of a given Batch object can be any of the following:

|  |  |
| --- | --- |
| **Status** | **Description** |
| **validating** | the input file is being validated before the batch can begin |
| **failed** | the input file has failed the validation process |
| **in\_progress** | the input file was successfully validated and the batch is currently being run |
| **finalizing** | the batch has completed and the results are being prepared |
| **completed** | the batch has been completed and the results are ready |
| **expired** | the batch was not able to be completed within the 24-hour time window |
| **cancelling** | the batch is being cancelled (may take up to 10 minutes) |
| **cancelled** | the batch was cancelled |

**#Listing Batch tasks and fetch the result**

batches = **client.batches.list**(limit=10)

for batch in batches.data:

    if batch.status == "in-progress":

        print(batch.id, " is in progress")

    #Checking the Status of a Batch

    if **batch.status == "completed"**:

        #Retrieving the batch results

        file\_response = client.files.content(batch**.output\_file\_id**)

        file\_content = file\_response.text

        lines = file\_content.splitlines()

        for line in lines:

            line\_json = json.loads(line)

            print(line\_json["response"]['body']['choices'][0]['message']['content'])

## **Rate Limits**

Batch API rate limits are separate from existing per-model rate limits. The Batch API has two new types of rate limits:

1. **Per-batch limits:** A single batch may include up to **50,000 requests**, and a batch input file can be up to **200 MB** in size. Note that **/v1/embeddings** batches are also restricted to a maximum of **50,000** embedding inputs across all requests in the batch.
2. **Enqueued prompt tokens per model:** Each model has a maximum number of Batch Queue Limits (tokens per day = TPD) allowed for batch processing. You can find these limits on the [Platform Settings page](https://platform.openai.com/settings/organization/limits).

There are **no limits for output tokens** or number of submitted requests for the Batch API today. Because Batch API rate limits are a new, separate pool, **using the Batch API will not consume tokens from your standard per-model rate limits**, thereby offering you a convenient way to increase the number of requests and processed tokens you can use when querying our API.

**Batch Expiration**

* Batches that do not complete in time eventually move to an **expired** state; unfinished requests within that batch are **cancelled**, and any responses to completed requests are made available via the batch's output file. You will be charged for tokens consumed from any completed requests.
* Expired requests will be written to your error file with the message as shown below. You can use the **custom\_id** to retrieve the request data for expired requests.

{"id": "batch\_req\_123", "custom\_id": "request-3", "response": null, "error": {"code": "**batch\_expired**", "message": "This request could not be executed before the completion window expired."}}

{"id": "batch\_req\_123", "custom\_id": "request-7", "response": null, "error": {"code": "**batch\_expired**", "message": "This request could not be executed before the completion window expired."}}

All in one Code

import openai

import json

from openai import OpenAI

import os

client = OpenAI()

def print\_batch\_level\_errors(batch):

    if not batch.errors or not batch.errors.data:

        return

    print("Batch Errors:")

    for error in batch.errors.data:

        print(

            f"Line={error.line} Code={error.code} Param={error.param} Message={error.message}"

        )

def print\_completed\_responses(batch):

    if batch.status != "completed" or not batch.output\_file\_id:

        return

    file\_response = client.files.content(batch.output\_file\_id)

    file\_content = file\_response.text

    lines = file\_content.splitlines()

    for line in lines:

        if line.strip():

            line\_json = json.loads(line)

            print("Response: ", line\_json["response"])

            print(line\_json["response"]["body"]["choices"][0]["message"]["content"])

            print("--------------------")

def print\_failed\_request\_reasons(batch):

    if batch.errors and batch.errors.data:

        print\_batch\_level\_errors(batch)

        print("--------------------")

    if not batch.error\_file\_id:

        print("No batch error file is available for this batch.")

        return

    file\_response = client.files.content(batch.error\_file\_id)

    file\_content = file\_response.text

    lines = file\_content.splitlines()

    if not any(line.strip() for line in lines):

        print("The batch error file is empty.")

        return

    print("Failed Request Reasons:")

    for line in lines:

        if not line.strip():

            continue

        line\_json = json.loads(line)

        custom\_id = line\_json.get("custom\_id", "N/A")

        response = line\_json.get("response") or {}

        error = line\_json.get("error") or response.get("body", {}).get("error", {})

        status\_code = response.get("status\_code", "N/A")

        error\_code = error.get("code", "N/A") if isinstance(error, dict) else "N/A"

        error\_message = error.get("message", "Unknown error") if isinstance(error, dict) else str(error)

        error\_param = error.get("param", "N/A") if isinstance(error, dict) else "N/A"

        print(f"Custom ID: {custom\_id}")

        print(f"Status Code: {status\_code}")

        print(f"Error Code: {error\_code}")

        print(f"Param: {error\_param}")

        print(f"Reason: {error\_message}")

        print("--------------------")

def upload\_file\_and\_create\_batch():

    # Upload batch tasks file

    with open("mybatch.jsonl", "rb") as f:

        batch\_input\_file = client.files.create(

            file=f,

            purpose="batch"

        )

    print("File uploaded with ID: ", batch\_input\_file.id)

    # Create and execute a batch from an uploaded file of requests

    batch = client.batches.create(

        input\_file\_id=batch\_input\_file.id,

        endpoint="/v1/chat/completions",

        completion\_window="24h",

        metadata={

            "description": "nightly eval job"

        }

    )

    print("Batch created with ID: ", batch.id)

    return batch

def print\_batch\_ids():

    batches = client.batches.list(limit=10)

    for batch in batches: #["data"]:

        print(f"Batch Id= {batch.id} Status= {batch.status}")

def print\_batch\_details(batch\_id):

    batch = client.batches.retrieve(batch\_id)

    print("Status=", batch.status)

    print("Total Tasks: ", batch.request\_counts.total)

    print("Completed Tasks: ", batch.request\_counts.completed)

    print("Failed Tasks: ", batch.request\_counts.failed)

    print\_batch\_level\_errors(batch)

    print\_completed\_responses(batch)

def print\_failed\_batch\_reason(batch\_id):

    batch = client.batches.retrieve(batch\_id)

    print("Status=", batch.status)

    print("Failed Tasks: ", batch.request\_counts.failed)

    print\_failed\_request\_reasons(batch)

def get\_batch\_id\_from\_user():

    batch\_id = input("Enter batch ID: ")

    return batch\_id

def delete\_batch(batch\_id):

    client.batches.delete(batch\_id)

    print("Batch deleted")

def main():

    print("Select an option:")

    print("1. Upload File and Create Batch")

    print("2. Get Batch Ids")

    print("3. Print Batch Details")

    print("4. Print Failed Batch Reason")

    choice = input("Enter your choice: ")

    if choice == '1':

        upload\_file\_and\_create\_batch()

    elif choice == '2':

        print\_batch\_ids()

    elif choice == '3':

        batch\_to\_print = get\_batch\_id\_from\_user()

        print\_batch\_details(batch\_to\_print)

    elif choice == '4':

        batch\_to\_print = get\_batch\_id\_from\_user()

        print\_failed\_batch\_reason(batch\_to\_print)

    else:

        print("Invalid choice")

# Run the main function

main()