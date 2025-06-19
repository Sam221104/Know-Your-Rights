# <p align="center"><img src="just_is.gif" alt="Logo" width="80"/><br><strong><span style="font-size: 24px;"> Know Your Rights</span></strong></p>


Know Your Rights is an AI-powered legal assistant that helps users understand their rights under the **Indian Penal Code (IPC)**. The chatbot provides information on fundamental rights, legal procedures, and human rights protections using a knowledge base of Indian legal documents. You can simply ask a question in plain language — like whether a certain action is a crime or what a specific law means — and the chatbot will provide a clear, structured explanation, including punishments, examples, and related laws. Whether you're a student, a concerned citizen, or just curious about your rights, this tool makes complex legal information easy to access and understand.

**Live Website:** [https://samsylvester-knowyourrights.streamlit.app/](https://samsylvester-knowyourrights.streamlit.app/)

## 📸 Demo

https://github.com/user-attachments/assets/8eb23117-a2a4-4625-b376-77197ef67d79

---
## Project Structure
```
Know-Your-Rights/
├── app.py              # Main Streamlit app
├── process_pdfs.py     # Script to generate FAISS index
├── formatter.py        # Formatter using Gemini LLM
├── just_is.gif         # Visual logo/animation
├── requirements.txt    # Dependencies list
├── .env                # API key config (user-provided)
├── docs/               # Folder for legal PDFs
│   └── Indian Penal Code.pdf
├── faiss_index/        # FAISS vector index files
│   ├── index.faiss
│   └── index.pkl
└── src/
    └── helper.py       # Embedding + retrieval logic
```
---
## How It Works
 1. **PDF Preprocessing:** IPC PDFs are loaded and split into chunks. Each chunk is converted into numerical embeddings using HuggingFace (all-MiniLM-L6-v2).
 2. **Vector Storage (FAISS):** The embeddings are stored in FAISS, a fast vector database that allows semantic search.
 3. **User Input via Streamlit:** Users ask legal questions through a chat interface built with Streamlit.
 4. **Semantic Retrieval:** The question is embedded and compared to the FAISS index to fetch the most relevant IPC sections.
 5. **Initial Response (LLM 1):** A lightweight local model (Flan-T5) generates a basic natural language answer from the retrieved content.
 6. **Structured Formatting (LLM 2):** The answer is passed to Gemini 1.5 Flash, which reformats it into a clean legal structure that is easily understood.
 7. **Conversational Memory:** Using LangChain’s memory module, chat history is preserved for follow-up questions.
---
## Detailed Tech Stack
### 1. **Streamlit**
- **Why:** Provides a fast, interactive, and easy-to-use web interface for Python applications.
- **How:** Used to build the chatbot UI, display responses, and manage user input/output in real time.
### 2. **PyPDF2**
- **Why:** Efficiently extracts text from PDF documents.
- **How:** Parses the IPC and other legal PDFs, splitting them into manageable text chunks for further processing.
### 3. **Sentence Transformers (all-MiniLM-L6-v2)**
- **Why:** Converts text into dense vector embeddings that capture semantic meaning.
- **How:** Each chunk of legal text is embedded so that similar questions and legal sections are close in vector space, enabling semantic search.
### 4. **FAISS (Facebook AI Similarity Search)**
- **Why:** Provides fast and scalable similarity search over large collections of vectors.
- **How:** Stores all legal text embeddings, allowing the system to quickly retrieve the most relevant sections for any user query.
### 5. **Flan-T5 (google/flan-t5-small)**
- **Why:** Lightweight, open-source LLM fine-tuned for instruction following and question answering.
- **How:** Generates initial answers to user questions based on the retrieved legal text, ensuring responses are relevant and concise.
### 6. **Gemini 1.5 Flash (via Google API)**
- **Why:** Advanced LLM capable of understanding context and *formatting complex information.**
- **How:** Reformats the initial answer into a structured, easy-to-understand legal summary (with punishments, explanations, and examples).
### 7. **LangChain**
- **Why:** Simplifies LLM orchestration, memory management, and chaining multiple models.
- **How:** Maintains conversational memory, manages prompt templates, and coordinates the flow between retrieval, answer generation, and formatting.
### 8. **python-dotenv**
- **Why:** Securely manages API keys and environment variables.
- **How:** Loads sensitive credentials (like the Gemini API key) from a `.env` file, keeping them out of source code.
### 9. **FAISS Index Preprocessing Script**
- **Why:** Precomputes and stores vector embeddings for all legal documents.
- **How:** `process_pdfs.py` reads PDFs, splits them, embeds each chunk, and saves the FAISS index for fast runtime retrieval.
### 10. **Helper Scripts (src/helper.py, formatter.py)**
- **Why:** Modularizes code for embedding, retrieval, and formatting logic.
- **How:** 
  - `helper.py` handles embedding and semantic search.
  - `formatter.py` uses Gemini to structure the output.
---
## Tech Stack
- Frontend: Streamlit
- LLMs: Flan-T5 (google/flan-t5-small), Gemini 1.5 Flash
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Vector DB: FAISS
- PDF Parsing: PyPDF2
- Env Config: python-dotenv

## 🔧 Installation Guide
### 1. Clone the Repository
```
git clone [https://github.com/Sam221104/Know-Your-Rights.git](https://github.com/Sam221104/Know-Your-Rights.git)
cd Know-Your-Rights
```
### 2. Set Up a Virtual Environment
On Windows:
```
python -m venv .venv
Set-ExecutionPolicy Unrestricted -Scope Process
.venv\Scripts\Activate
```
On macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```
### 3. Install Dependencies
```
pip install --upgrade pip
pip install -r requirements.txt
```
### 4. Add Your API Key
Create a .env file in the root directory with the following:
```GOOGLE_API_KEY=your_google_gemini_api_key_here```
### 5. Preprocess Legal PDFs for faster response
```
python process_pdfs.py
```
This reads IPC PDFs from the docs/ folder and builds a FAISS index using HuggingFace embeddings.
### 6. Run the Application
```
streamlit run app.py
```
#### This launches the interface at ```http://localhost:8501.```
---
## Features

- **Ask Legal Questions** in natural language
- **Semantic Search** across IPC sections using FAISS and HuggingFace embeddings
- **Structured Summaries** with punishments, explanation, and example cases
- **Conversational Memory** to retain chat history
---
## Project Summary
Know Your Rights is a digital assistant that helps people easily understand their legal rights under the Indian Penal Code. By allowing users to ask questions in everyday language, it provides clear and concise explanations of laws, punishments, and legal procedures. This tool empowers individuals to make informed decisions, promotes legal awareness, and helps bridge the gap between complex legal language and the general public. Whether you are a student, a concerned citizen, or someone seeking guidance, Know Your Rights makes legal information accessible and understandable for everyone.



