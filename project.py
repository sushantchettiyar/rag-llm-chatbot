import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="RAG LLM Chatbot", page_icon="🤖", layout="centered")
st.title("🤖 RAG LLM Chatbot")
st.markdown("### Ask questions about the document: *data/llm.pdf*")
st.caption("Powered by LlamaIndex • Ollama (tinyllama) • sentence-transformers")

# -------------------------------
# Load Models and Index (Cached)
# -------------------------------
@st.cache_resource(show_spinner="Loading models and indexing document...")
def load_models_and_index():
    # 1. Embedding model (lightweight and fast)
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 2. Use tinyllama — perfect for low RAM systems
    try:
        from llama_index.llms.ollama import Ollama

        Settings.llm = Ollama(
            model="tinyllama",            # ← Changed to tinyllama
            request_timeout=300.0,
            temperature=0.7,
        )
    except ImportError:
        st.error("Missing package: Run `pip install llama-index-llms-ollama`")
        st.stop()

    # 3. Load your PDF document
    try:
        documents = SimpleDirectoryReader(input_files=["data/llm.pdf"]).load_data()
        if not documents:
            st.error("No content found in 'data/llm.pdf'. Check the file path.")
            st.stop()
    except Exception as e:
        st.error(f"Error loading PDF: {e}")
        st.stop()

    # 4. Build the vector index
    index = VectorStoreIndex.from_documents(documents)

    # 5. Create query engine with streaming
    query_engine = index.as_query_engine(
        similarity_top_k=3,
        streaming=True,
    )

    return query_engine

# Load everything (only once)
query_engine = load_models_and_index()

# -------------------------------
# Chat History
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm a lightweight RAG chatbot using TinyLlama. Ask me anything about *llm.pdf*! 😊"
    })

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# User Input & Streaming Response
# -------------------------------
if prompt := st.chat_input("Ask a question about the document..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and stream response
    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""

        with st.spinner("Thinking..."):
            response_stream = query_engine.query(prompt)

            for token in response_stream.response_gen:
                full_response += token
                placeholder.markdown(full_response + "▌")  # Blinking cursor effect

            placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit • LlamaIndex • Ollama (TinyLlama)")