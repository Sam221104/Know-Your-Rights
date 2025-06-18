# <p align="center"><img src="just_is.gif" alt="Logo" width="80"/><br><strong><span style="font-size: 24px;"> Know Your Rights</span></strong></p>


Know Your Rights is an AI-powered legal assistant that helps users understand their rights under the **Indian Penal Code (IPC)**. The chatbot provides information on fundamental rights, legal procedures, and human rights protections using a knowledge base of Indian legal documents. You can simply ask a question in plain language — like whether a certain action is a crime or what a specific law means — and the chatbot will provide a clear, structured explanation, including punishments, examples, and related laws. Whether you're a student, a concerned citizen, or just curious about your rights, this tool makes complex legal information easy to access and understand.

---

## 📸 Demo



---

## 🚀 Features

- 🔍 **Ask Legal Questions** in natural language
- 📚 **Semantic Search** across IPC sections using FAISS and HuggingFace embeddings
- 📖 **Structured Summaries** with punishments, explanation, and example cases
- 🧠 **Conversational Memory** to retain chat history

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
1. PDF Preprocessing: IPC PDFs are loaded and split into chunks. Each chunk is converted into numerical embeddings using HuggingFace (all-MiniLM-L6-v2).
2. Vector Storage (FAISS): The embeddings are stored in FAISS, a fast vector database that allows semantic search.
3. User Input via Streamlit: Users ask legal questions through a chat interface built with Streamlit.
4. Semantic Retrieval: The question is embedded and compared to the FAISS index to fetch the most relevant IPC sections.
5. Initial Response (LLM 1): A lightweight local model (Flan-T5) generates a basic natural language answer from the retrieved content.
6. Structured Formatting (LLM 2): The answer is passed to Gemini 1.5 Flash, which reformats it into a clean legal structure that is easily understood.
7. Conversational Memory: Using LangChain’s memory module, chat history is preserved for follow-up questions.

## 📦 Tech Stack
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
5. Preprocess Legal PDFs for faster response
```
python process_pdfs.py
```
This reads IPC PDFs from the docs/ folder and builds a FAISS index using HuggingFace embeddings.
6. Run the Application
```
streamlit run app.py
```
This launches the interface at ```http://localhost:8501.```


🔐 License
This project is intended for educational and research use only. Please follow government and legal guidelines for data use.

🙌 Credits
Hugging Face Transformers & Sentence Transformers
Google Gemini API (via LangChain)
FAISS by Facebook
Indian Government legal PDFs (IPC)
✊ “Own your rights. Defend your freedom.” — Know Your Rights
