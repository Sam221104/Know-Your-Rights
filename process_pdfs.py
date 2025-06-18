import os
from src.helper import get_pdf_text, get_text_chunks, get_vector_store, save_vector_store

# Define the directory where your source PDFs are located
PDF_DIRECTORY = "docs" # Create a 'docs' folder and put your PDFs here
FAISS_INDEX_PATH = "faiss_index" # Folder to save the FAISS index

def process_and_save_docs():
    pdf_paths = []
    if not os.path.exists(PDF_DIRECTORY):
        print(f"Error: PDF directory '{PDF_DIRECTORY}' not found. Please create it and place your PDFs inside.")
        return

    for filename in os.listdir(PDF_DIRECTORY):
        if filename.endswith(".pdf"):
            pdf_paths.append(os.path.join(PDF_DIRECTORY, filename))

    if not pdf_paths:
        print(f"No PDF files found in '{PDF_DIRECTORY}'. Please add some PDFs.")
        return

    opened_pdf_docs = []
    try:
        for p_path in pdf_paths:
            opened_pdf_docs.append(open(p_path, 'rb'))

        print(f"Processing {len(opened_pdf_docs)} PDF(s)...")
        raw_text = get_pdf_text(opened_pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        vector_store = get_vector_store(text_chunks) # This uses the HF embeddings
        save_vector_store(vector_store, FAISS_INDEX_PATH)
        print("PDFs processed and vector store saved successfully!")
    except Exception as e:
        print(f"An error occurred during processing: {e}")
    finally:
        for f in opened_pdf_docs:
            f.close()

if __name__ == "__main__":
    process_and_save_docs()