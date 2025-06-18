import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough

# Load .env file at the very start of this module
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please set the GOOGLE_API_KEY environment variable in your .env file.")

# Initialize the Gemini LLM once for the formatter
# Using gemini-1.5-flash for faster, cost-effective summaries
formatter_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", # Use the model that worked
    temperature=0.3, # Keep low for strict formatting adherence
    max_output_tokens=500, # Increased tokens to allow for more detailed output
    google_api_key=GOOGLE_API_KEY
)

# Define the specific IPC formatting prompt
IPC_FORMATTING_PROMPT_TEMPLATE = """
You are a highly experienced legal expert and formatter specializing in the Indian Penal Code (IPC). Your primary goal is to present IPC section information in a clear, concise, and structured format.

**Conditional Initial Response:**
- **IF** the `Original Question` asks whether a *particular action or scenario* is offensive or a crime (e.g., "someone trespasses burial ground," "is it legal to hit someone?"), then begin your answer with:
  "**Yes**, [brief answer about offensiveness] under Section [relevant IPC section number] IPC."
  OR
  "**No**, [brief answer about offensiveness] under Section [relevant IPC section number] IPC."
  (Choose Yes/No based on whether the action is indeed an offense. If it's a general question not directly about an offense, omit this line and proceed to the main format.)

- **IF** the `Original Question` *directly references an IPC section number* (e.g., "What is Section 302 IPC?", "Explain Section 498A"), then **DO NOT** include the "Yes/No" initial response. Proceed directly to the "Section [number] IPC:" line.


Here is the exact format you MUST follow:

Section [number, **Crucially, identify the PRECISE IPC section number based on the `Original Question` first. If the `Raw Content` clearly and definitively refers to a different section, prioritize that. Otherwise, rely on your knowledge.**] IPC: [title, provide the official title of the identified section]

Explanation:
[Provide a concise 2-3 line plain English summary of the identified section's scope and purpose.]

Key Details:
- [Essential element 1: State a crucial component or condition of the identified section.]
- [Essential element 2: State another crucial component or condition.]
- [Essential element 3: State a third crucial component or condition. If fewer than 3 are applicable or available, provide what is relevant.]

Punishment:
[State the exact punishment clause(s) for the identified section, including imprisonment terms(in numbers) and fines.]

Example Case Study:
- [Describe a hypothetical or generalized scenario (1-2 sentences) where this identified section would typically apply. For instance: "In a case of theft involving movable property...", or "If an individual causes grievous hurt..."]

Relevant Sections:
[If applicable, list any other IPC sections ONLY that are commonly associated with or referenced in relation to the identified section. If none, dont mention the this part.]

**Important Instructions:**
1.  **Prioritize the Requested Section:** Your ultimate goal is to provide accurate information for the IPC section implied or explicitly stated in the `Original Question`.
2.  **Utilize Raw Content Strategically:**
    * **IF** the `Raw Content` (marked as {text} below) *directly and comprehensively* addresses the IPC section from the `Original Question`, use it as your primary source for all fields.
    * **IF** the `Raw Content` is *insufficient, incomplete, or ambiguous* regarding the section from the `Original Question`, or if the `Original Question` is about a section *not clearly present* in the `Raw Content`, then **supplement or generate information for all fields using your comprehensive legal knowledge of the Indian Penal Code to ensure a complete and accurate answer for the requested section.**
    * **IF** the `Raw Content` seems *irrelevant or contradictory* to the `Original Question` (e.g., asking about Section 296 but the raw text is primarily about Section 297), **prioritize generating the answer for the `Original Question`'s section using your knowledge, and ignore the misleading parts of the `Raw Content`.**

3.  **Strict Formatting:** Maintain the exact headings, bullet points, and structure as provided in the format.
4.  **Conciseness:** Be brief and to the point for each section.
5.  **Citations:** Remove all external citations, e.g., (1999) or [12].

Original Question: {question_asked}
Raw Content for Formatting:
{text}
"""
ipc_formatting_prompt = PromptTemplate(
    input_variables=["text"],
    template=IPC_FORMATTING_PROMPT_TEMPLATE
)

# Create the formatting chain using LCEL
ipc_formatting_chain = ipc_formatting_prompt | formatter_llm

def format_retrieved_docs(retrieved_docs: list, original_question: str) -> str: # ADDED original_question here
    
    if not retrieved_docs:
        # If no docs are retrieved, still try to answer based on the question_asked and LLM's knowledge
        raw_content = "No relevant documents were retrieved. Relying on general IPC knowledge."
    else:
        raw_content = " ".join([doc.page_content for doc in retrieved_docs])

    try:
        # Invoke the LCEL chain with both inputs
        formatted_output = ipc_formatting_chain.invoke({
            "text": raw_content,
            "question_asked": original_question # Pass the original question here
        })
        return formatted_output
    except Exception as e:
        print(f"Error formatting retrieved documents: {e}")
        # Consider a more user-friendly error message for the UI
        return f"Failed to format document due to an internal error. Please try again. Error: {e}"
