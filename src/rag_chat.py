from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate


# Load environment variables
load_dotenv()


# Load embedding model
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Load FAISS vector database
db = FAISS.load_local(
    "vectorstore",
    embedding_model,
    allow_dangerous_deserialization=True
)


# Create retriever
retriever = db.as_retriever(
    search_kwargs={"k": 5}
)


# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2
)


# Prompt template
prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a medical AI assistant specialized in Parkinson's Disease.

Use ONLY the provided context to answer the user's question.

If the answer is not present in the context, say:
"I could not find sufficient information in the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""
)


def ask_question(question):
    """
    Retrieve relevant documents and generate an answer.
    """

    # Retrieve top 5 relevant chunks
    docs = retriever.invoke(question)

    # Build context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Create final prompt
    final_prompt = prompt.format(
        context=context,
        question=question
    )

    # Generate response
    response = llm.invoke(final_prompt)

    # Collect source file names
    sources = []
    for doc in docs:
        source = doc.metadata.get("source", "Unknown")
        sources.append(source)

    return response.content, sources


# Run only in terminal
if __name__ == "__main__":

    question = input("Enter your question: ")

    answer, sources = ask_question(question)

    print("\n" + "=" * 60)
    print("Answer")
    print("=" * 60)
    print(answer)

    print("\n" + "=" * 60)
    print("Retrieved Sources")
    print("=" * 60)

    for i, source in enumerate(sources, start=1):
        print(f"{i}. {source}")