import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load .env file
load_dotenv()

# Read API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("GOOGLE_API_KEY not found!")

# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=api_key
)

# Test Question
response = llm.invoke("What are the symptoms of Parkinson's disease?")

print("\nGemini Response:\n")
print(response.content)