import os
import shutil
import stat
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language
from langchain_community.document_loaders import GitLoader
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
# JSON parsers
from langchain_core.output_parsers import JsonOutputParser
from langchain.output_parsers import OutputFixingParser
from langchain_core.runnables import RunnablePassthrough

# RAG Chain Setup

# Load env variables & retrieve API key
load_dotenv()
if os.environ.get("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")


# Handle directory deletions
def delete_dir(func, path, exc):
    if not os.access(path, os.W_OK):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


# Ingest Cacher
prev_ingest_url = None

# Initialize LLM & Embedding models
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", max_output_tokens=1024)
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# Initialize prompt
# Prompt template
template = """
You are an expert AI pair programmer and codebase analyst.
Your primary goal is to help users understand their codebase.

You must follow these rules strictly:
1.  **Analyze the Context:** Base your answer exclusively on the code provided in the 'Context'.
2.  **Cite Your Sources:** Quote the exact relevant code snippet from the context that supports your answer.
3.  **Handle Insufficient Context:** If the context is insufficient, the value for the "explanation" key must be "The provided context does not contain enough information to answer this question.", and the "fileName" and "codeSnippet" keys must be empty strings.
4.  **Be Concise:** Keep your explanation to 2-3 sentences. For the "codeSnippet", select only the most crucial and relevant lines of code (Up to 30 lines maximum) that directly answer the question. Do not include boilerplate or irrelevant surrounding code.

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


# Ingestion logic
def ingest_repo(repoURL: str) -> None:
    REPO_PATH = "./temp_repo"
    DB_PATH = "./chroma_db"

    # Remove/clean old directories
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH, onexc=delete_dir)
    if os.path.exists(REPO_PATH):
        shutil.rmtree(REPO_PATH, onexc=delete_dir)

    # Use GitLoader to clone and load repo
    loader = GitLoader(
        repo_path=REPO_PATH,
        clone_url=repoURL,
        branch="main",
        file_filter=lambda file_path: file_path.endswith(".py")
    )
    documents = loader.load()

    # Split code into chunks
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1000,
        chunk_overlap=100,
    )
    chunked_documents = splitter.split_documents(documents)

    # Create ChromaDB vector store and store in ./chroma_db"
    db = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )

    # Clean up the cloned repo
    shutil.rmtree(REPO_PATH, onexc=delete_dir)
    print("Completed Ingestion")


# Initialize Flask app
app = Flask(__name__)
CORS(app)


# API endpoint to handle ingestion of URL
@app.route('/ingest', methods=['POST'])
def ingest():
    global prev_ingest_url

    data = request.get_json()
    repo_url = data.get('repo_url')

    if not repo_url:
        return jsonify({"error": "No repository URL provided"}), 400

    # Caching ingestion
    if repo_url == prev_ingest_url:
        print('Already ingested')
        return jsonify({"status": "success", "message": f"Repository {repo_url} is already ingested."})

    try:
        ingest_repo(repo_url)
        prev_ingest_url = repo_url
        return jsonify({"status": "success", "message": f"Successfully ingested {repo_url}"})
    except Exception as e:
        return jsonify({"error": f"Failed to ingest repository: {str(e)}"}), 500


# API endpoint to handle Q&A portion
@app.route('/ask', methods=['POST'])
def ask():
    # Get data from request
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "No Question Provided"}), 400

    try:
        db = Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings
        )

        # Improved parser
        output_parser = OutputFixingParser.from_llm(
            parser=JsonOutputParser(),
            llm=llm
        )

        retriever = db.as_retriever(search_kwargs={"k": 10})

        rag_chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | output_parser
        )

        # Invoke RAG chain
        result_json = rag_chain.invoke(question)

        return jsonify(result_json)
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Run app
if __name__ == '__main__':
    app.run(debug=True, port=5000)
