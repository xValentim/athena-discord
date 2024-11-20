# Personalized Newsletter Bot for Discord

## Project Description

The **Personalized Newsletter Bot** is a Discord-based chatbot designed to streamline information aggregation and personalized content delivery. Users can send URLs from web pages or YouTube videos to the bot, which extracts the content (text or transcriptions) and stores it for future use. Periodically, the bot generates a **personalized newsletter** for subscribed users, summarizing the content accumulated during the period and delivering it in an easily digestible format on email. 

This project use natural language processing (NLP) techniques, including text summarization, and personalization, to address the pain point of managing and consuming vast amounts of online content efficiently.

---

## Category and Goal

This project follow the **Blue Sky Developer** category.

### Final Goal:
To demonstrate the viability of this approach in solving the user pain point of managing and consuming large amounts of online content. The success will be measured by:
- **User Impact**: At least 70% of beta testers reporting that the bot reduces their time spent managing online content in a survey.

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

``TODO``

---

## Technical Approach

### 1. Content Extraction:
   - **Web Scraping**: BeautifulSoup and LangChain for HTML parsing and text extraction.
   - **Transcription**: Trancript-YouTube-API for converting YouTube video to text.

### 2. Summarization:
   - **Model**: OpenAI (gpt-4o-mini) or Groq (Llama 3.2/3.1).
   - **Evaluation**: 

### 3. Personalization:
   - **Newsletter Generation**: Uses stored content to generate personalized newsletters.

### 4. Delivery:
   - **Discord Integration**: Built using `discord.py` for seamless interaction and newsletter delivery.

---

## Deliverables

1. **Code Repository**:
   - Complete implementation of the bot, including extraction, summarization, and newsletter generation.

2. **Impact Assessment**:
   - Results from beta testers, including user feedback surveys.
   - X score evaluation for summarization.

3. **Video Pitch**:
   - A 3-minute video demonstrating the bot, summarization quality, and user impact metrics.

---

## How This Project Meets the Rubric

``TODO``

---

## Getting Started

### Prerequisites
- Python 3.8+
- Libraries: `requirements.txt`

### Setup

``TODO``
---

## Future Improvements

``TODO``