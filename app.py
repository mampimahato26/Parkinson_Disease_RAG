import streamlit as st
from src.rag_chat import ask_question

# ---------------------------------------
# Page Configuration
# ---------------------------------------
st.set_page_config(
    page_title="Parkinson Disease RAG Chatbot",
    page_icon="🧠",
    layout="wide"
)

# ---------------------------------------
# Session State
# ---------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None

# ---------------------------------------
# Sidebar
# ---------------------------------------
with st.sidebar:

    st.title("🧠 Parkinson RAG")

    st.markdown("---")

    st.subheader("About")

    st.write(
        """
This chatbot answers Parkinson's Disease questions using
Retrieval-Augmented Generation (RAG),
FAISS Vector Database,
Sentence Transformers,
and Google Gemini AI.
"""
    )

    st.markdown("---")

    st.subheader("Sample Questions")

    sample_questions = [
        "🩺 What are the symptoms of Parkinson's disease?",
        "🔍 How is Parkinson's disease diagnosed?",
        "💊 What treatments are available?",
        "❓ Can Parkinson's disease be cured?",
        "⚠️ What are the early symptoms?",
        "💉 What medications are used?"
    ]

    for q in sample_questions:

        clean_question = q[2:]  # Remove emoji

        if st.button(q, use_container_width=True):
            st.session_state.selected_question = clean_question

    st.markdown("---")

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.selected_question = None
        st.rerun()

    st.markdown("---")

    st.caption("Built with ❤️ using Streamlit • LangChain • FAISS • Gemini")

# ---------------------------------------
# Main UI
# ---------------------------------------
st.title("🧠 Parkinson Disease RAG Chatbot")

st.caption("AI-powered Medical Assistant using RAG + Google Gemini")

st.write("Ask any question related to Parkinson's Disease.")

# ---------------------------------------
# Display Previous Messages
# ---------------------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant" and "sources" in message:

            with st.expander("📄 Retrieved Sources"):

                for source in message["sources"]:
                    st.write(source)

# ---------------------------------------
# Chat Input
# ---------------------------------------
question = st.chat_input(
    "Ask anything about Parkinson's Disease..."
)

if st.session_state.selected_question:

    question = st.session_state.selected_question
    st.session_state.selected_question = None

# ---------------------------------------
# Generate Response
# ---------------------------------------
if question:

    # User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Assistant Message
    with st.chat_message("assistant"):

        with st.spinner("Searching medical documents..."):

            answer, sources = ask_question(question)

            unique_sources = list(dict.fromkeys(sources))

            st.markdown(answer)

            with st.expander("📄 Retrieved Sources"):

                for source in unique_sources:
                    st.write(source)

    # Save Assistant Message
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": unique_sources
        }
    )