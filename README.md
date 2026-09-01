# Parkinson's Disease – Evidence-Based Clinical Decision Support System

An Evidence-Based Clinical Decision Support System for Parkinson's Disease using **Retrieval-Augmented Generation (RAG)**.

The system retrieves relevant medical information from a Parkinson's Disease knowledge base and uses the retrieved context to generate evidence-grounded responses with Google Gemini.

---

## 📌 Project Overview

Medical information related to Parkinson's Disease is often distributed across different documents and sources, making it difficult to quickly find relevant and reliable information.

This project addresses this problem by combining:

- Document processing
- Text chunking
- Sentence Transformer embeddings
- FAISS vector similarity search
- Retrieval-Augmented Generation (RAG)
- Google Gemini for response generation
- Streamlit for the user interface

The system first retrieves relevant medical information and then generates a context-aware response based on the retrieved evidence.

---

## 🎯 Objectives

- Retrieve relevant Parkinson's Disease information efficiently.
- Reduce unsupported or hallucinated responses from general-purpose LLMs.
- Provide evidence-grounded medical responses.
- Build an interactive clinical decision-support interface.
- Evaluate the system using a set of Parkinson's Disease test queries.

---

## 🏗️ System Architecture

```text
Parkinson's Disease Medical Documents
                │
                ▼
       Document Processing
      (Loading + Chunking)
                │
                ▼
       Sentence Transformer
          Embeddings
                │
                ▼
          FAISS Vector
           Database
                │
                ▼
       Relevant Top-5 Sources
                │
                ▼
      Context + User Query
                │
                ▼
        Google Gemini LLM
                │
                ▼
     Evidence-Grounded Response
                │
                ▼
          Streamlit UI