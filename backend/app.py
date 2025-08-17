import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# RAG Chain Setup

# Load env variables
load_dotenv()

# Gemini API for embeddings
if os.environ.get("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")

# Initialize LLM & Embedding models
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Load ChromaDB vector store
db = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
)

# Create retriever
retriever = db.as_retriever(
    search_kwargs={"k": 10},
)

# Prompt template
template = """
You are an expert AI pair programmer and codebase analyst.
Your primary goal is to help users understand their codebase.

You must follow these rules strictly:
1.  **Analyze the Context:** Base your answer exclusively on the code provided in the 'Context'.
2.  **Cite Your Sources:** Quote the exact relevant code snippet from the context that supports your answer.
3.  **Handle Insufficient Context:** If the context is insufficient, the value for the "explanation" key must be "The provided context does not contain enough information to answer this question.", and the "fileName" and "codeSnippet" keys must be empty strings.

**JSON Output Format:**
You MUST format your entire response as a single JSON object with the following keys:
- "explanation": A detailed, direct answer to the user's question.
- "fileName": The name of the file where the relevant code is located.
- "codeSnippet": The exact code snippet from the context that supports your answer.

**Example Response:**
{{
  "explanation": "The `get_order_details` function retrieves all items associated with a specific order ID by performing a SQL query that joins the `order_details` and `products` tables.",
  "fileName": "main.py",
  "codeSnippet": "def get_order_details(connection, order_id):\\n    cursor = connection.cursor()\\n    query = (\\"SELECT o.order_id, o.quantity, o.total_price, p.name, p.price_per_unit FROM order_details o LEFT JOIN products p on o.product_id = p.product_id where o.order_id = %s\\")\\n    cursor.execute(query, (order_id,))\n    # ...rest of the function..."
}}

Context: 
{context}

Question:
{question}
"""
prompt = PromptTemplate.from_template(template)

# Build RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print("Finished initializing models and RAG Chain setup")


# Initialize Flask app
app = Flask(__name__)
CORS(app)


# /help API endpoint
@app.route('/help', methods=['POST'])
# Handle POST requests to /help
def help():
    print("Received help request")

    # Get data from request
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No Question Provided"}), 400

    print(f"Question: {question}")

    # Invoke RAG chain
    result = rag_chain.invoke(question)
    print(f"AI Response: {result}")

    # Parse AI response to JSON
    try:
        result_json = json.loads(result)
        return jsonify(result_json)
    except json.JSONDecodeError as e:
        return jsonify({"error": "Failed to parse AI response as JSON"}), 500


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
