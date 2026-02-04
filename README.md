# 🦅 Cyber News RAG

**Automated Vulnerability Analysis System powered by Retrieval-Augmented Generation**

An intelligent security analysis pipeline that collects **real vulnerability reports** from the HackerOne API, processes them using modern RAG architecture, and provides expert-level threat analysis using Local AI (Ollama).

> 🔗 **Every response includes clickable source links** to real HackerOne reports for verification.

## ✨ Key Features

- **Real Data**: Fetches actual disclosed vulnerability reports from HackerOne Hacktivity API
- **Local AI**: Uses Ollama (Llama3) for privacy-respecting, offline-capable analysis
- **Source Citation**: Every response includes links to the original HackerOne reports
- **Red Team Perspective**: Analysis includes root cause, OWASP mapping, and detection recommendations
- **Smart Routing**: LLM-based query router decides optimal retrieval strategy

## 🏗️ Architecture

```
[HackerOne API] → [Chunking] → [Embeddings] → [Qdrant Vector Store]
                                                        ↓
[User Query] → [Smart Router] → [HyDE Retrieval] → [Ollama LLM] → [Response + Sources]
```

### Pipeline Components

1. **Collector**: Direct integration with HackerOne Hacktivity API (with fallback to mock data)
2. **Processing**: Recursive chunking to preserve technical context
3. **Embeddings**: `all-MiniLM-L6-v2` for high-performance vector generation
4. **Vector Store**: Qdrant for persistent storage and fast similarity search
5. **Retrieval**: HyDE (Hypothetical Document Embeddings) for improved semantic matching
6. **Generation**: Ollama (Llama3) or Google Gemini for expert-level analysis

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.com/)** (for Local AI) OR **Google Gemini API Key** (for Cloud AI).
- **Chrome Browser** (for Selenium scraping).

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

    - **Option A: Local AI (Recommended & Free)** 🦙
        1. Install [Ollama](https://ollama.com/).
        2. Pull a model (e.g., Llama 3): `ollama pull llama3`
        3. The project is configured to use `llama3` by default.

    - **Option B: Cloud AI (Gemini)** ☁️
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

- Integration with Telegram/Discord bots for real-time alerts.
- "Agentic Chunking" full implementation.
- Evaluation dashboard comparing RAG strategies.

---
*Developed for Cyber Security Portfolio.*
