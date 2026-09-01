from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Load PDFs
loader = PyPDFDirectoryLoader("data/Parkinson_Disease")
documents = loader.load()

print("Total documents loaded:", len(documents))

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents)

print("Total chunks created:", len(chunks))

# Show first chunk
print("\nFirst chunk preview:\n")
print(chunks[0].page_content[:500])