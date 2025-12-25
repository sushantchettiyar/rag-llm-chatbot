# 🤖 RAG LLM Chatbot

A simple **Retrieval-Augmented Generation (RAG)** chatbot built with:
- **Streamlit** (web interface)
- **LlamaIndex** (RAG framework)
- **Ollama** (local LLM runner with **TinyLlama** model – perfect for low-RAM machines)
- **sentence-transformers** (embeddings)

This app lets you ask questions about a specific PDF document loaded into the knowledge base.

**Live Repo**: https://github.com/sushantchettiyar/rag-llm-chatbot

## 🚀 Features
- Fully local – no API keys or cloud needed
- Streaming responses for a chat-like feel
- Lightweight (uses TinyLlama: ~1-2 GB RAM)
- Easy to customize the input document

## 📄 Knowledge Base (Data Given to the Model)

The chatbot **only** has knowledge from the document located at:
data/llm.pdf
text- This PDF is the **only data source** indexed and provided to the LLM via retrieval.
- The app loads it once at startup using LlamaIndex's `SimpleDirectoryReader`.
- All answers are based on retrieved chunks from this single file + generation by TinyLlama.
- **No internet access, no other training data** – responses are grounded in `llm.pdf` content only.

> **How to check what data is used?**  
> Open the file `data/llm.pdf` in the repository (or locally). That's exactly what the model "knows" about!

If you want to use a different document:
1. Replace `data/llm.pdf` with your own PDF.
2. Restart the app – it will automatically index the new file.

## 🛠️ Setup & Run Locally

### Prerequisites
1. Install **Ollama**: https://ollama.com/download
2. Pull the lightweight model:
   ```bash
   ollama pull tinyllama

Start Ollama server (it runs in background on Windows/Mac/Linux).

Installation
Bash# Clone the repo
git clone https://github.com/sushantchettiyar/rag-llm-chatbot.git
cd rag-llm-chatbot

# (Recommended) Create a virtual environment
python -m venv vnv
source vnv/bin/activate    # On Windows: vnv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
Run the App
Bashstreamlit run project.py
The app will open in your browser (usually http://localhost:8501). Start chatting!
