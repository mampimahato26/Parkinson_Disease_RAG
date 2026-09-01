from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

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
retriever = db.as_retriever(search_kwargs={"k": 5})

# Test query
query = "What are the symptoms of Parkinson's disease?"

# Retrieve relevant documents
docs = retriever.invoke(query)

print("=" * 80)
print("User Query:")
print(query)
print("=" * 80)

for i, doc in enumerate(docs, start=1):
    print(f"\nResult {i}")
    print("-" * 80)
    print("Source:", doc.metadata.get("source", "Unknown"))
    print("\nContent:\n")
    print(doc.page_content[:800])