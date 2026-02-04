# 🦅 Cyber News RAG

**Automated Vulnerability Analysis System powered by Retrieval-Augmented Generation**

Cyber News RAG is a sophisticated intelligence pipeline that collects, synthesizes, and analyzes security reports (specifically from HackerOne Hacktivity) to provide actionable insights. Built with a modern Agentic RAG architecture, it leverages LLMs to decode complex attack vectors and suggest defenses.

## 🏗️ Architecture

The system follows a modular "Authentic RAG" pipeline:

1. **Collector**: Automated scraping of vulnerability reports (Selenium/BeautifulSoup).
2. **Processing**: Advanced chunking strategies (Recursive, Semantic) to preserve technical context.
3. **Embeddings**: High-performance vector generation using `sentence-transformers` (all-MiniLM-L6-v2).
4. **Vector Store**: Persistent storage and retrieval-ready indexing with **Qdrant**.
5. **Retrieval Engine**:
    * **HyDE (Hypothetical Document Embeddings)**: Generates synthetic technical descriptions to improve semantic match.
    * **Hybrid Search**: Combines keyword filtering with dense vector similarity.
    * **Router Agent**: An LLM-based router decides whether to query the knowledge base, search the web, or answer directly.
6. **LLM Synthesis**: Uses **Google Gemini 1.5 Pro** to generate professional analyst-grade summaries and mitigation strategies.

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **LLM**: Google Gemini (via `google-generativeai`)
* **Vector DB**: Qdrant
* **Frameworks**: LangChain, LlamaIndex concepts
* **ML**: Sentence Transformers (HuggingFace)
* **Scraping**: Selenium, BeautifulSoup
* **Orchestration**: AsyncIO, Schedule

## 🚀 Getting Started

### Prerequisites

* **Python 3.10+**
* **[Ollama](https://ollama.com/)** (for Local AI) OR **Google Gemini API Key** (for Cloud AI).
* **Chrome Browser** (for Selenium scraping).

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/cyber-news-rag.git
    cd cyber-news-rag
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. **Setup AI Engine**:

    * **Option A: Local AI (Recommended & Free)** 🦙
        1. Install [Ollama](https://ollama.com/).
        2. Pull a model (e.g., Llama 3): `ollama pull llama3`
        3. The project is configured to use `llama3` by default.

    * **Option B: Cloud AI (Gemini)** ☁️
        1. Copy the example env file: `cp .env.example .env` (or manually rename).
        2. Edit `config/settings.yaml` and change `provider` to `gemini`.
        3. Add your key to `.env`: `GOOGLE_API_KEY=your_key_here`.

### Usage

**Run the Pipeline (Ingest + Query):**

```bash
python main.py "How to prevent Stored XSS in React applications?"
```

**Run the Scheduler (Continuous Ingestion):**

```bash
python scheduler.py
```

## 📂 Project Structure

```text
cyber-news-rag/
├── src/
│   ├── collector/      # Scraping & Data Loading
│   ├── processing/     # Chunking & Embedding
│   ├── storage/        # Vector Database (Qdrant)
│   ├── retrieval/      # Search logic (HyDE, Hybrid)
│   ├── llm/            # LLM Integration (Gemini)
│   └── evaluation/     # QA & benchmarking tools
├── config/             # Settings
├── main.py             # CLI Entry point
└── scheduler.py        # Background job runner
```

## 🔮 Future Improvements

* Integration with Telegram/Discord bots for real-time alerts.
* "Agentic Chunking" full implementation.
* Evaluation dashboard comparing RAG strategies.

---
*Developed for Cyber Security Portfolio.*
