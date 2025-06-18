import streamlit as st
import os
from dotenv import load_dotenv
from src.helper import load_vector_store, get_conversational_chain
from formatter import format_retrieved_docs
from langchain_core.messages import AIMessage, HumanMessage
import base64

st.set_page_config(page_title="Know Your Rights", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #121212 !important;
            color: #E0E0E0 !important;
        }

        .block-container {
            padding-top: 8rem !important;
            padding-bottom: 7rem !important;
            max-width: 1000px;
            margin: 0 auto !important;
            background-color: #121212 !important;
        }

        .header-fixed {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 9999;
            padding: 1rem 2rem;
        }

        .circular-image {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 50% !important;
            border: 2px solid #4CAF50;
            display: block;
        }

        .complaint-button {
            background-color: #e53935;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            margin-top: 20px;
            cursor: pointer;
            border-radius: 8px;
            border: none;
            text-align: center;
        }

        .stForm.st-emotion-cache-qcpnpn.e1ttwmlf1 {
            position: fixed !important;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            background-color: #1e1e1e !important;
            padding: 10px 20px;
            border: 1px solid #444;
            border-radius: 12px;
            box-shadow: 0px 0px 10px rgba(255,255,255,0.05);
            z-index: 9999;
        }

        .stTextInput input {
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #555;
            background-color: #222 !important;
            color: #eee !important;
        }

        button[kind="primary"] {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            margin-left: 10px;
        }

        button {
            background-color: #333 !important;
            color: #eee !important;
        }

        .stMarkdown, .stText, .stHeading, .stSubheader, .stCaption {
            color: #E0E0E0 !important;
        }

        ::-webkit-scrollbar {
            width: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #555; 
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #888; 
        }
    </style>
""", unsafe_allow_html=True)

load_dotenv()
FAISS_INDEX_PATH = "faiss_index"

@st.cache_resource
def setup_backend_resources():
    with st.spinner("Loading legal knowledge base..."):
        vector_store = load_vector_store(FAISS_INDEX_PATH)
        if vector_store:
            return get_conversational_chain(vector_store)
        else:
            st.error("Error: Knowledge base not found or could not be loaded.")
            return None

@st.cache_data
def _get_gif_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        st.error(f"GIF file not found: {path}")
        return ""

def handle_user_input_callback():
    user_question = st.session_state.user_input_text_form
    if user_question:
        st.session_state.chatHistory.append(HumanMessage(content=user_question))
        st.session_state.pending_answer = user_question

def clear_conversation_callback():
    st.session_state.clear_flag = True

def main():
    gif_base64 = _get_gif_base64("just_is.gif")
    st.markdown(f"""
    <div class="header-fixed" style="background: transparent;">
        <div style="
            max-width: 60%;
            margin: 0 auto;
            background-color: #1e1e1e;
            padding: 1rem 2rem;
            border-radius: 12px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <div style="display: flex; align-items: center; gap: 10px;">
                <img src="data:image/gif;base64,{gif_base64}" class="circular-image">
                <div style="line-height: 1.2;">
                    <h1 style='color: #4CAF50; margin: 0;'>Know Your Rights</h1>
                    <p style='font-size: 1.1em; font-style: italic; color: #ccc; margin: 2px 0 0 0;'>\"Own your rights, defend your freedom.\"</p>
                </div>
            </div>
            <div>
                <a href='https://hrcnet.nic.in/HRCNet/public/Home.aspx' target='_blank'>
                    <button class='complaint-button'>File a Complaint</button>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if "chatHistory" not in st.session_state:
        st.session_state.chatHistory = []
    if "user_input_text_form" not in st.session_state:
        st.session_state.user_input_text_form = ""
    if "conversation_chain" not in st.session_state:
        st.session_state.conversation_chain = setup_backend_resources()
    if "clear_flag" not in st.session_state:
        st.session_state.clear_flag = False
    if "pending_answer" not in st.session_state:
        st.session_state.pending_answer = None

    # --- Chat History ---
    for message in st.session_state.chatHistory:
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        else:
            with st.chat_message("assistant"):
                st.write(message.content)

    # --- Spinner & LLM Response ---
    if st.session_state.pending_answer:
        user_question = st.session_state.pending_answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if st.session_state.conversation_chain is None:
                    st.session_state.chatHistory.append(AIMessage(content="Error: Knowledge base not ready."))
                    st.session_state.pending_answer = None
                    st.rerun()

                retrieved_docs = st.session_state.conversation_chain.retriever.get_relevant_documents(user_question)
                raw_llm_response_message = format_retrieved_docs(retrieved_docs, user_question)
                formatted_reply_string = raw_llm_response_message.content if hasattr(raw_llm_response_message, 'content') else str(raw_llm_response_message)

                import time

                ai_placeholder = st.empty()
                lines = formatted_reply_string.strip().split('\n')
                final_output = ""

                for line in lines:
                    current_line = ""
                    for char in line:
                        current_line += char
                        ai_placeholder.markdown(final_output + current_line + "▌")
                        time.sleep(0.009)  # Typing speed per character
                    final_output += current_line + "\n"
                    ai_placeholder.markdown(final_output + "▌")

                # Final display without cursor
                ai_placeholder.markdown(final_output)

                st.session_state.chatHistory.append(AIMessage(content=formatted_reply_string))

        st.session_state.pending_answer = None
        st.rerun()

    # --- Input Form ---
    with st.form("chat_form", clear_on_submit=True):
        input_col, send_col, clear_col = st.columns([6, 1.5, 1.5])
        with input_col:
            st.text_input(
                "Ask a Question:",
                key="user_input_text_form" if not st.session_state.get("clear_flag") else "temp_clear_key",
                placeholder="Type your legal question here...",
                label_visibility="collapsed"
            )

        with send_col:
            st.form_submit_button("Send", use_container_width=True, on_click=handle_user_input_callback)
        with clear_col:
            st.form_submit_button("Clear", use_container_width=True, on_click=clear_conversation_callback)

    # --- Clear Chat ---
    if st.session_state.clear_flag:
        st.session_state.chatHistory = []
        st.session_state.clear_flag = False
        st.rerun()

if __name__ == "__main__":
    main()
