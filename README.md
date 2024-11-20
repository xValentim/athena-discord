# Personalized Newsletter Bot for Discord

## Project Description

The **Personalized Newsletter Bot** is a Discord-based chatbot designed to streamline information aggregation and personalized content delivery. Users can send URLs from web pages or YouTube videos to the bot, which extracts the content (text or transcriptions) and stores it for future use. Periodically, the bot generates a **personalized newsletter** for subscribed users, summarizing the content accumulated during the period and delivering it in an easily digestible format on email. 

This project use natural language processing (NLP) techniques, including text summarization, and personalization, to address the pain point of managing and consuming vast amounts of online content efficiently.

---

## Category and Goal

This project follow the **Blue Sky Developer** category.

### Final Goal:
To demonstrate the viability of this approach in solving the user pain point of managing and consuming large amounts of online content. The success will be measured by:
- **User Impact**: At least **70%** of beta testers reporting that the bot reduces their time spent managing online content in a survey.

### Evaluation Metrics

To ensure the quality and relevance of the summaries generated by the system, we evaluate the performance of the summarization module using the following method:

1. **Embedding Generation**:
   - We generate embeddings for both the original content and the summarized content using OpenAIEmbeddings. 

2. **Cosine Similarity**:
   - The similarity between the original content and its corresponding summary is computed using the **cosine similarity** metric. This measures how close the two embeddings are in the vector space, where a value of 1 indicates identical content and a value of 0 indicates no similarity.

3. **Satisfactory Threshold**:
   - If the cosine similarity between the original and summarized embeddings is **above 0.6**, the summary is considered **satisfactory**.
   - If the cosine similarity is **below 0.6**, the summary is considered **unsatisfactory**.

4. **Overall Evaluation**:
   - The percentage of satisfactory summaries is calculated as:
     \[
     \text{Satisfactory Percentage} = \frac{\text{Number of Satisfactory Summaries}}{\text{Total Summaries}} \times 100
     \]
   - This percentage serves as the **primary evaluation metric** for the system. It provides a clear and interpretable measure of how well the summaries retain the meaning and relevance of the original content.

### Why This Metric?
This approach ensures that the system's performance is evaluated based on semantic retention rather than surface-level lexical similarity. The threshold of 0.6 is chosen to allow for some variation in the wording while still capturing the essence of the content.

#### Result Metrics

The system reach a satisfactory percentage of **~84%** or higher to demonstrate the effectiveness of the summarization module in preserving the meaning and relevance of the original content. More detail you can find in ``notebooks/metrics.ipynb``.

#### Result Impact

The system will be considered successful if the satisfactory percentage is above the threshold of **70%**. This indicates that the summaries generated by the system are of sufficient quality to be useful to users in reducing the time spent managing and consuming online content.

---

## Key Features

1. **Content Extraction**:
   - Web pages: Extracts and cleans text from provided URLs.
   - YouTube videos: Transcribes audio using YouTube API.
   
2. **Summarization**:
   - Summarizes the extracted content using LLM-based summarization techniques via API(e.g., OpenAI and Groq).

3. **Periodic Newsletter Delivery**:
   - Aggregates summarized content into a concise, personalized newsletter delivered at regular intervals.

---

## Research and Related Work

About **summarization** tasks, there are several approaches to summarization but many content about it is relatively old and not up-to-date. Two works that are relevant to this project are:

1. [Benchmarking Large Language Models for News Summarization](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00632/119276/Benchmarking-Large-Language-Models-for-News): This paper evaluates the performance of large language models on news summarization tasks and provides insights into the capabilities and limitations of these models. The content is a bit old, comparing models like GPT3-Davinci and BRIO, for example. However it can be useful to understand more about summarization tasks.

---

## Technical Approach

### 1. Content Extraction:
   - **Web Scraping**: BeautifulSoup and LangChain for HTML parsing and text extraction.
   - **Transcription**: Trancript-YouTube-API for converting YouTube video to text.

### 2. Summarization:
   - **Model**: OpenAI (gpt-4o-mini) or Groq (Llama 3.2/3.1).
   - **Evaluation**: Comparative between models using cosine similarity (our metric: **~84%**).

### 3. Delivery:
   - **Discord Integration**: Built using `discord.py` for seamless interaction and newsletter delivery.
   - **Email Delivery**: Using SMTP for sending newsletters to subscribed users.
   - **FastAPI with Cron Jobs**: For scheduling and periodic newsletter generation.

---

## Deliverables

1. **Code Repository**:
   - Complete implementation of the bot, including extraction, summarization, and newsletter generation.

2. **Impact Assessment**:
   - Results from beta testers, including user feedback surveys.
   - Evaluation metrics comparing embeddings and cosine similarity.

3. **Video Pitch**:
   - A 3-minute video demonstrating the bot, summarization quality, and user impact metrics. You can acces it [here]().