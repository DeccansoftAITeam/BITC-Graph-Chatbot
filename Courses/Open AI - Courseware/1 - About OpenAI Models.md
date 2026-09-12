**About OpenAI**

* What is OpenAI
* OpenAI Models
* What is Token?

What is Open AI

* OpenAI, founded in **December 2015** is a private research organization and technology company that develops **AI-powered products** and tools that benefits humanity:
* It is committed to ensure AI is developed and used **Ethical** to mitigate potential risks.
* Originally a non-profit, OpenAI transitioned to a “**capped-profit**” model to attract investment for large-scale AI projects. Balances research with developing market-leading AI solutions like GPT and DALL·E.

**Founders**: Elon Musk, Sam Altman, Greg Brockman.

**OpenAI has partnered with Microsoft** is a Strategic partnership with a $1 billion investment. Integration of OpenAI models into Azure AI services.

**Types of OpenAI Models**

1. **Frontier / Flagship Models**

* Most advanced reasoning, understanding, instruction-following, multimodal support, large context windows, best for complex tasks, coding, agentic workflows.
* Strong general intelligence and versatile across domains (text, code, vision, etc.).

Example Models:

* GPT-5.2 (best overall; excels at reasoning & coding)
* GPT-5.2-pro (higher precision & more compute)
* GPT-5.1 family (previous flagship)
* GPT-5 (earlier flagship)

1. **General-Purpose / Instruction Models**

* Great for conversational AI, instruction following, summarization, Q&A, and broad usage.
* Large context windows for longer inputs.

Example Models:

* GPT-4.1 (high-quality text & instruction tasks)
* GPT-4.1 mini & nano (more cost-efficient / faster variants)

1. **Reasoning / Task-Focused Models**

* Enhanced reasoning depth and problem solving — useful for science, math, logic, and complex decisions.
* Often optimized for multi-step chain of thought reasoning.

Example Models:

* o3 (deep reasoning model)
* o4-mini (fast & affordable reasoning)
* o3-mini (cost-efficient reasoning)

1. **Realtime & Audio/Multimodal Models**

* Support real-time text & audio processing, speech-to-text, text-to-speech, and multimodal interactions.

Example Models:

* gpt-realtime (real-time text & audio)
* gpt-realtime-mini (cost-efficient realtime)
* gpt-audio & gpt-audio-mini (audio-centric)
* GPT-4o Audio & mini variants (voice + text)

1. **Vision & Image Models**

* Vision understanding, image analysis, and generation. Useful for multimodal AI apps involving pictures.

Example Models:

* DALL·E 3 (current image-generation model)
* GPT Image 1.5 (updated image generation)
* chatgpt-image-latest (image model in ChatGPT)

1. **Embeddings Models**

* Produce vector embeddings for search, clustering, similarity, retrieval, classification.
* Used widely in semantic search and recommendation systems.

Example Models:

* text-embedding-3-large (most capable)
* text-embedding-3-small (cost-efficient)

1. **Open-Weight / Research Models**

* Models with weights released openly to enable deployment on personal hardware and research fine-tuning.
* Designed for broader accessibility and experimentation.

Example Models:

* gpt-oss-120b (high-performance open model)
* gpt-oss-20b (smaller, mobile/edge use)

1. **Specialized Tool & Moderation Models**

* Specific roles like content moderation, real-time computer interface tasks, specialized API workflows.

Example Models:

* omni-moderation (content moderation)
* computer-use-preview (tools & workflows)

1. **Open Weight Models by OpenAI:**

* Designed for agentic tasks: Leverage powerful instruction following and tool use within the chain-of-thought, including web search and Python code execution.
* Deeply customizable: Adjust the reasoning effort to low, medium, or high. Plus, customize the models to adapt to your use case with full-parameter fine-tuning.
* Playground: <https://gpt-oss.com/>
* Full chain-of-thought: Access the full chain-of-thought for easier debugging and higher trust in model outputs.

Example Models:

* gpt-oss-120b
* gpt-oss-20b

Choosing a model

A key choice to make when generating content through the API is which model you want to use –

* **Reasoning models** generate an internal chain of thought to analyze the input prompt, and excel at understanding complex tasks and multi-step planning. They are also generally slower and more expensive to use than GPT models.
* **GPT models** are fast, cost-efficient, and highly intelligent, but benefit from more explicit instructions around how to accomplish tasks.
* **Large and small (mini or nano) models** offer trade-offs for speed, cost, and intelligence. Large models are more effective at understanding prompts and solving problems across domains, while small models are generally faster and cheaper to use.

**Models Documentation:**

<https://platform.openai.com/docs/models/>

**Comparing Models:**

<https://platform.openai.com/docs/models/compare>

What is Token?

**Token is** a **unit of text** that the model processes. It can be as small as a single character or as large as a whole word, depending on the **context** and **language**.

Tokens are not cut up exactly where the words start or end - tokens can include trailing spaces and even sub-words.

The sentence “**ChatGPT is great!**” is broken into tokens like:

* “Chat”, “GPT”, “ is”, “ great”, “!”.

Here are some helpful rules of thumb for understanding tokens in terms of lengths:

* 1 token ~= 4 chars in English ~= ¾ words
* 100 tokens ~= 75 words

Or

* 1-2 sentence ~= 30 tokens
* 1 paragraph ~= 100 tokens
* 1,500 words ~= 2048 tokens

How words are split into tokens is also language-dependent. For example ‘Cómo estás’ (‘*How are you*’ in Spanish) contains 5 tokens (for 10 chars) आप कैसे हैं? Contains 3 tokens (11 chars). The higher token-to-char ratio can make it more expensive to implement the API for languages other than English.

**Tokenizer tool** (<https://platform.openai.com/tokenizer>), allows you to calculate the number of tokens

Please note that the exact tokenization process varies between models.

Alternatively, if you'd like to tokenize **text programmatically**, use [Tiktoken](https://github.com/openai/tiktoken) as a fast BPE tokenizer specifically used for OpenAI models.

**Token Types:**

* **Prompt tokens** are the tokens that you input into the model. This is the number of tokens in your prompt.
* **Completion tokens** are any tokens that the model generates in response to your input. For a standard request, this is the number of tokens in the completion.

**Pricing Calculation based on tokens:**

<https://platform.openai.com/docs/pricing>

**Rate Limit:**

<https://platform.openai.com/docs/guides/rate-limits>