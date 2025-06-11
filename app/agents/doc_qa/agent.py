import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.groq import Groq
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
from app.core.config import settings as app_settings

def create_doc_qa_engine():
    """
    Creates a RAG query engine using LlamaIndex.
    It reads documents from the './data' directory, indexes them,
    and prepares a query engine.
    """
    print("Creating Document Q&A engine...")

    # 1. Configure the LLM we want to use for GENERATION
    llm = Groq(model="llama3-70b-8192", api_key=app_settings.GROQ_API_KEY)

    # 2. Configure the Embedding Model we want to use for INDEXING
    # "local:BAAI/bge-small-en-v1.5" tells LlamaIndex to download this
    # small, powerful embedding model and run it locally. No API key needed.
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    # 3. Apply these settings globally for LlamaIndex
    Settings.llm = llm
    Settings.embed_model = embed_model
    print("LLM and local embedding model configured.")

    # The rest of the function is the same
    if not os.path.exists("data"):
        raise FileNotFoundError(
            "The 'data' directory was not found. Please create it and add a text file."
        )

    documents = SimpleDirectoryReader("data").load_data()
    print(f"Loaded {len(documents)} document(s).")

    index = VectorStoreIndex.from_documents(documents)
    print("Vector store index created in memory.")

    query_engine = index.as_query_engine()
    print("Document Q&A engine is ready.")

    return query_engine