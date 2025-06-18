# ⚖️ Know Your Rights – Legal Information Retrieval System

Know Your Rights is an AI-powered legal assistant that helps users understand their rights under the **Indian Penal Code (IPC)**. 
The chatbot provides information on fundamental rights, legal procedures, and human rights protections using a knowledge base of Indian legal documents.

---

## 📸 Demo

![Demo](just_is.gif)

---

## 🚀 Features

- 🔍 **Ask Legal Questions** in natural language
- 📚 **Semantic Search** across IPC sections using FAISS and HuggingFace embeddings
- 📖 **Structured Summaries** with punishments, explanation, and example cases
- 🧠 **Conversational Memory** to retain chat history

---

## 🧾 Project Structure

Know-Your-Rights/
├── app.py              # Main Streamlit app
├── process_pdfs.py     # Script to generate FAISS index
├── formatter.py        # Formatter using Gemini LLM
├── just_is.gif         # Visual logo/animation
├── requirements.txt    # Dependencies list
├── .env                # API key config
│
├── docs/               # Folder for legal PDFs
│   └── Indian Penal Code.pdf
├── faiss_index/        # FAISS vector index
│
└── src/
└── helper.py       # Embedding + retrieval logic

---

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

### How It Works
1. User asks a legal question
2. FAISS retrieves relevant IPC sections from indexed PDFs
3. HuggingFace LLM generates a basic answer
4. Gemini LLM formats it with section number, explanation, punishment, and related sections
5. Results are displayed in the Streamlit chat interface with memory support

### 📦 Tech Stack
- Frontend: Streamlit
- LLMs: Flan-T5 (google/flan-t5-small), Gemini 1.5 Flash
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- Vector DB: FAISS
- PDF Parsing: PyPDF2
- Env Config: python-dotenv

🔐 License
This project is intended for educational and research use only. Please follow government and legal guidelines for data use.

🙌 Credits
Hugging Face Transformers & Sentence Transformers
Google Gemini API (via LangChain)
FAISS by Facebook
Indian Government legal PDFs (IPC)
✊ “Own your rights. Defend your freedom.” — Know Your Rights
