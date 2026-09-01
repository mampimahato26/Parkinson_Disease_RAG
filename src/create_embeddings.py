from sentence_transformers import SentenceTransformer
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDFs
loader = PyPDFDirectoryLoader("data/Parkinson_Disease")
documents = loader.load()

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks:", len(chunks))

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Test embedding
embedding = model.encode(chunks[0].page_content)

print("\nEmbedding dimension:", len(embedding))
print("First 10 values:\n")
print(embedding[:10])