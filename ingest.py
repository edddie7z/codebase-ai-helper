import os
import shutil
import stat
from dotenv import load_dotenv
from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Load env variables
load_dotenv()

# Gemini API for embeddings
if os.environ.get("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")

# GitHub repo to use as example
REPO_URL = "https://github.com/codebasics/python_projects_grocery_webapp.git"
TEMP_REPO_PATH = "./temp_repo"
print(f"Cloning repository from {REPO_URL}...")


# Use GitLoader to clone and load repo
# Only include Python files
loader = GitLoader(
    repo_path=TEMP_REPO_PATH,
    clone_url=REPO_URL,
    branch="main",
    file_filter=lambda file_path: file_path.endswith(".py")
)
documents = loader.load()
print(f"Loaded {len(documents)} documents.")


# Split code into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
)

chunked_documents = splitter.split_documents(documents)
print(f"Split {len(documents)} document(s) into {len(chunked_documents)} chunks.")

# Embed and store in ChromaDB
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("Embedding model initialized.")

# Create ChromaDB vector store and store in ./chroma_db"
print("Creating and storing embeddings in ChromaDB...")
db = Chroma.from_documents(
    documents=chunked_documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)
print("Embeddings stored in ChromaDB.")


# Clean/delete temp repo
def handle_remove_readonly(func, path, exc):
    if not os.access(path, os.W_OK):
        # path is read-only, so change permissions and retry
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        raise


try:
    shutil.rmtree(TEMP_REPO_PATH, onexc=handle_remove_readonly)
    print(f"Deleted temporary repository directory: {TEMP_REPO_PATH}")
except OSError as e:
    print(f"Error deleting temporary directory: {e}")
