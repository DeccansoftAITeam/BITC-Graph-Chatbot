File Management in OpenAI

Files are uploaded assets you want the model or tools to reference later.

They are **inputs to other capabilities**.

**Common purposes**

|  |  |
| --- | --- |
| **Purpose** | **Used for** |
| assistants | RAG / document grounding |
| fine-tune | Training datasets |
| batch | Batch API jobs |
| vision | Image understanding |
| responses | Multi-modal Responses API |

| **Limit** | **Typical** |
| --- | --- |

|  |  |
| --- | --- |
| Max file size | ~512 MB (varies by use) |

|  |  |
| --- | --- |
| Tokenized text | Counts toward context |

|  |  |
| --- | --- |
| File count | Account-level limits |

**Files API Retention Rules**

1. **Files with purpose="batch"**
   * These files **automatically expire after 30 days** by default.
   * You can explicitly control this using the expires\_after parameter when uploading.
   * After expiration, the file becomes inaccessible.
2. **Files with other purposes (e.g., fine-tuning, embeddings, assistants, etc.)**
   * These are **persisted indefinitely — until you explicitly delete them**.
   * OpenAI does *not* automatically delete such files based solely on age

from openai import OpenAI

import os

# Initialize OpenAI client

client = OpenAI(api\_key=os.getenv("OPENAI\_API\_KEY"))

class OpenAIFileManager:

    @staticmethod

    def upload\_file():

        filepath = input("Enter path of file to upload: ")

        if not os.path.isfile(filepath):

            print("File does not exist.")

            return

        purpose = input("Enter purpose user\_data | vision | fine-tune | batch (default = 'user\_data'): ") or "user\_data"

        try:

            with open(filepath, "rb") as f:

                response = client.files.create(file=f, purpose=purpose)

            print(f"Uploaded: ID = {response.id} | Name = {response.filename}")

        except Exception as e:

            print(f"Error uploading file: {e}")

    @staticmethod

    def list\_files():

        try:

            files = client.files.list()

            if not files.data:

                print("No files found.")

                return

            print("\nAvailable Files:")

            for f in files.data:

                print(f"ID: {f.id} | Name: {f.filename} | Purpose: {f.purpose} | Status: {f.status}")

        except Exception as e:

            print(f"Error listing files: {e}")

    @staticmethod

    def retrieve\_file\_content():

        file\_id = input("Enter file ID: ")

        try:

            file\_content = client.files.content(file\_id).read().decode('utf-8')

            print("\nFile Content:")

            print(file\_content)

        except Exception as e:

            print(f"Error retrieving content: {e}")

    @staticmethod

    def download\_file():

        file\_id = input("Enter file ID: ")

        destination = input("Enter destination path (e.g., output.jsonl): ")

        try:

            file\_content = client.files.content(file\_id)

            with open(destination, "wb") as f:

                f.write(file\_content.read())

            print(f"File downloaded to {destination}")

        except Exception as e:

            print(f"Error downloading file: {e}")

    @staticmethod

    def delete\_file():

        file\_id = input("Enter file ID to delete: ")

        try:

            response = client.files.delete(file\_id)

            print(f"Deleted file: {file\_id} | Status: {response.deleted}")

        except Exception as e:

            print(f"Error deleting file: {e}")

def main():

    manager = OpenAIFileManager()

    while True:

        print("\n===== OpenAI File Manager Menu =====")

        print("1. Upload a File")

        print("2. List All Files")

        print("3. Retrieve File Content")

        print("4. Download a File")

        print("5. Delete a File")

        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':

            manager.upload\_file()

        elif choice == '2':

            manager.list\_files()

        elif choice == '3':

            manager.retrieve\_file\_content()

        elif choice == '4':

            manager.download\_file()

        elif choice == '5':

            manager.delete\_file()

        elif choice == '6':

            print("Exiting. Goodbye!")

            break

        else:

            print("Invalid choice. Please enter a number between 1 and 6.")

if \_\_name\_\_ == "\_\_main\_\_":

    main()

**Using files with the Responses API (modern way)**

**Example pattern**

{

"model": "...",

"input": [

{

"role": "user",

"content": [

{ "type": "text", "text": "Summarize this document" },

**{ "type": "input\_file", "file\_id": "file\_abc123" }**

]

}

]

}

Generating response based on PDF content

OpenAI models can accept PDF files as input. Provide PDFs either as Base64-encoded data or as file IDs obtained after uploading files to the **/v1/files** endpoint through the [API](https://platform.openai.com/docs/api-reference/files) or [dashboard](https://platform.openai.com/storage/files/).

from openai import OpenAI

client = OpenAI()

file = client.files.create(

    file=open("OpenAI.pdf", "rb"),

    purpose="user\_data"

)

completion = client.chat.completions.create(

    model="gpt-4o",

    messages=[

        {

            "role": "user",

            "content": [

                {

                    "type": "file",

                    "file": {

                        "file\_id": file.id,

                    }

                },

                {

                    "type": "text",

                    "text": "Who are founders of OpenAI in the book?",

                },

            ]

        }

    ]

)

print(completion.choices[0].message.content)

print("Total Tokens: ", completion.usage.total\_tokens)

client.files.delete(file.id)

**Usage Consideration about files:**

* To help models understand PDF content, we put into the model's context both **extracted text and an image of each page**—regardless of whether the page includes images.
* You can upload **up to** 100 pages and 32MB of total content in a single request to the API, across multiple file inputs.
* Only models that support both text and image inputs, such as gpt-4o, gpt-4o-mini, or o1, and gpt-5.x can accept PDF files as input.
* You can upload these files to the Files API with any purpose, but we recommend using the **user\_data purpose** for files you plan to use as model inputs.

**Base64-encoded files:**

import base64

from openai import OpenAI

client = OpenAI()

filename = input("Enter filename: ")

with open(filename, "rb") as f:

    data = f.read()

base64\_string = base64.b64encode(data).decode("utf-8")

completion = client.chat.completions.create(

    model="gpt-5.6-luna",

    messages=[

        {

            "role": "user",

            "content": [

                {

                    "type": "file",

                    "file": {

                        "filename": filename,

                        "file\_data": f"data:application/pdf;base64,{base64\_string}",

                    }

                },

                {

                    "type": "text",

                    "text": "Compare all models of OpenAI",

                }

            ],

        },

    ],

)

print(completion.choices[0].message.content)