# backend/blob_utils.py

import json

from .azure_clients import blob_service_client

from . import config

from io import BytesIO

def load_schema_from_blob():

    """

    Downloads the schema blob (JSONL) and returns a list of dicts.

    Each line in the blob is expected to be a JSON object.

    """

    container_client = blob_service_client.get_container_client(config.SCHEMA_BLOB_CONTAINER)

    blob_client = container_client.get_blob_client(config.SCHEMA_BLOB_NAME)

    downloader = blob_client.download_blob()

    raw = downloader.readall()

    text = raw.decode("utf-8")

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

    docs = [json.loads(ln) for ln in lines]

    return docs

# small helper to create "content" from a doc if needed

def doc_to_content(doc: dict) -> str:

    """

    Convert one schema JSON object to a textual content string for RAG/indexing.

    Uses the provided 'content' field if present, else composes it.

    """

    if "content" in doc and doc["content"]:

        return doc["content"]

    # fallback compose

    cols = doc.get("columns", [])

    cols_text = "; ".join([f"{c.get('name')} ({c.get('datatype')}) - {c.get('description','')}" for c in cols])

    return f"Table {doc.get('tableName')}: {doc.get('description','')}. Columns: {cols_text}"
 