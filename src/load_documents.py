from langchain_community.document_loaders import PyPDFDirectoryLoader

# Load all PDFs recursively from the Parkinson_Disease folder
loader = PyPDFDirectoryLoader("data/Parkinson_Disease")

documents = loader.load()

print(f"Total documents loaded: {len(documents)}")

# Show first few documents
for i, doc in enumerate(documents[:5]):
    print(f"\nDocument {i+1}")
    print("Source:", doc.metadata["source"])