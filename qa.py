import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load env variables
load_dotenv()

# Gemini API for embeddings
if os.environ.get("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")

# Initialize LLM & Embedding models
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("Initalized models")

# Load ChromaDB vector store
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)
print("Loaded ChromaDB")

# Create retriever
retriever = db.as_retriever(
    search_kwargs={"k": 10},
)

# Prompt template
template = """
You are an expert helpful AI assistant that helps users find answers to questions on their codebase.

Answer the question based only on the following provided context.

If you don't know the answer, just say that you don't know. Don't try to make up an answer.

Context: 
{context}

Question:
{question}
"""
prompt = PromptTemplate.from_template(template)
print("Created prompt template")

# Build RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print("Built RAG chain")

# Example question
print("\nAsking question...")
question = "What does the function `get_order_details` do?"
result = rag_chain.invoke(question)

print("\nResult:")
print(result)
