import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings 
from langchain.llms import HuggingFacePipeline
from transformers import pipeline
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# --- Initialize HuggingFace Embeddings globally for consistency ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
    chunks = text_splitter.split_text(text)
    return chunks


def get_vector_store(text_chunks):
    # Generates a vector store (FAISS) from text chunks using the globally initialized HuggingFace Embeddings.
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings) # Use global embeddings
    return vector_store

def save_vector_store(vector_store, path="faiss_index"):
    #Saves a FAISS vector store to the specified path
    os.makedirs(path, exist_ok=True) # Ensure directory exists
    vector_store.save_local(path)
    print(f"Vector store saved to {path}")

def load_vector_store(path="faiss_index"):
    #Loads a FAISS vector store from the specified path.
    if not os.path.exists(path):
        print(f"Warning: Vector store not found at {path}. Please run initial processing script.")
        return None
    # Crucially, pass the same embeddings object used for creation
    loaded_vector_store = FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)
    print(f"Vector store loaded from {path}")
    return loaded_vector_store


def get_conversational_chain(vector_store):
    # Creates a conversational retrieval chain using a local HuggingFace LLM (google/flan-t5-small) and a vector store.
    
    llm_pipeline = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        tokenizer="google/flan-t5-small",
        max_new_tokens=500,
        temperature=0.7,
        do_sample=True,
    )
    llm = HuggingFacePipeline(pipeline=llm_pipeline)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain