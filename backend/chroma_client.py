# chroma_client.py
import os
from chromadb import PersistentClient
from backend import config
from backend.azure_clients import logger  # optional reuse of your logger

# config must define CHROMA_PERSIST_DIR and COLLECTION_NAME (fallback to INDEX_NAME)
PERSIST_DIR = getattr(config, "CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME = getattr(config, "INDEX_NAME", "qnxt-schema-collection")

# Create Chromadb client using new PersistentClient
_chroma_client = PersistentClient(path=PERSIST_DIR)

def get_client():
    return _chroma_client

def get_or_create_collection(name: str = COLLECTION_NAME, metadata: dict | None = None):
    """
    Returns a chroma collection. If not exists, create it.
    """
    client = get_client()
    try:
        # if exists, returns existing
        return client.get_collection(name)
    except Exception:
        # create collection
        return client.create_collection(name=name, metadata=metadata or {})



