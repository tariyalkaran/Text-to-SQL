# config.py
import os
from dotenv import load_dotenv

# Get absolute path to the project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
PROJECT_ROOT = os.path.dirname(BASE_DIR)               

load_dotenv()

# Azure OpenAI Config
OPENAI_API_TYPE = "azure"
OPENAI_API_BASE = os.getenv("AZURE_OPENAI_ENDPOINT") 
OPENAI_API_VERSION = "2023-05-15"
OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
EMBEDDING_DEPLOYMENT = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")

# Blob Storage
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
SCHEMA_BLOB_CONTAINER = os.getenv("SCHEMA_BLOB_CONTAINER")
SCHEMA_BLOB_NAME = os.getenv("SCHEMA_BLOB_NAME")


INDEX_NAME = os.getenv("ACS_INDEX_NAME", "qnxt-schema-collection")


# Chroma db
CHROMA_PERSIST_DIR = os.getenv(
   "CHROMA_PERSIST_DIR",
   os.path.join(PROJECT_ROOT, "backend", "schema_embeddings_store")
)
