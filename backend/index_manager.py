# index_manager.py

import json

from typing import List, Union

from backend.chroma_client import get_or_create_collection

from backend.embeddings import generate_embedding

from backend import config

from backend.azure_clients import logger  


EMBED_DIM = 1536

def _normalize_schema_input(schema: Union[str, List[dict], dict]) -> List[dict]:

    if isinstance(schema, str):

        s = schema.strip()

        if s.startswith("["):

            return json.loads(s)

        lines = [ln.strip() for ln in s.splitlines() if ln.strip()]

        return [json.loads(ln) for ln in lines]

    elif isinstance(schema, dict):

        if "Schema" in schema and isinstance(schema["Schema"], list):

            return schema["Schema"]

        return [schema]

    elif isinstance(schema, list):

        return schema

    else:

        raise ValueError("Unsupported schema input type")

def _normalize_columns(columns):

    normalized = []

    if not isinstance(columns, list):

        return normalized

    for c in columns:

        if not isinstance(c, dict):

            continue

        name = c.get("name") or c.get("COLUMN_NAME") or ""

        datatype = c.get("datatype") or c.get("DATA_TYPE") or ""

        nullable = c.get("nullable") or c.get("NULLABLE") or ""

        pkfk = c.get("pkfk") or c.get("PKFK") or ""

        col_desc = c.get("column_description") or c.get("description") or c.get("DESCRIPTION") or ""

        normalized.append({

            "name": name,

            "datatype": datatype,

            "nullable": nullable,

            "pkfk": pkfk,

            "column_description": col_desc

        })

    return normalized

def create_collection_if_not_exists(collection_name: str = None):

    name = collection_name or getattr(config, "INDEX_NAME", "qnxt-schema-collection")

    coll = get_or_create_collection(name=name, metadata={"source": "qnxt"})

    return coll

def upload_schema_to_collection(schema_input: Union[str, List[dict], dict], collection_name: str = None, batch_size: int = 256):

    """

    Upload the schema into Chroma collection. Each doc will store:

      id (str), tableName, table_description, columns (list), content (str), metadata dict

    """

    records = _normalize_schema_input(schema_input)

    collection = create_collection_if_not_exists(collection_name)

    ids = []

    metadatas = []

    documents = []

    embeddings = []

    skipped = 0

    for rec in records:

        if not isinstance(rec, dict):

            skipped += 1

            continue

        table_name = rec.get("tableName") or rec.get("TABLE_NAME") or rec.get("table_name")

        if not table_name:

            skipped += 1

            continue

        rid = rec.get("id") or table_name

        table_description = rec.get("table_description") or rec.get("description") or ""

        columns_raw = rec.get("columns") or []

        normalized_cols = _normalize_columns(columns_raw)

        # build content for embedding (prefer existing content)

        content = rec.get("content") or rec.get("content_text") or ""

        if not content:

            if normalized_cols:

                cols_txt = []

                for c in normalized_cols:

                    cn = c.get("name") or ""

                    cd = c.get("datatype") or ""

                    cdesc = c.get("column_description") or ""

                    cols_txt.append(f"{cn} ({cd}) - {cdesc}" if cn else f"{cdesc}")

                content = f"Table {table_name}: {table_description}. Columns: " + "; ".join(cols_txt)

            else:

                content = f"Table {table_name}: {table_description}"

        # generate embedding using your existing function

        try:

            emb = generate_embedding(content)

        except Exception as e:

            logger.exception("Embedding failed for %s: %s", table_name, e)

            skipped += 1

            continue

        if not isinstance(emb, list) or len(emb) != EMBED_DIM:

            logger.warning("Invalid embedding for %s; length=%s", table_name, getattr(emb, "__len__", lambda: None)())

            skipped += 1

            continue

        # prepare Chroma fields

        ids.append(str(rid))

        # store the readable doc text in documents (for fallback lexical search)

        documents.append(content)

        # store relevant metadata for retrieval & display

        metadatas.append({

            "tableName": table_name,

            "table_description": table_description,

            "columns": json.dumps(normalized_cols),

            "source": json.dumps(rec.get("metadata")  or {})

        })

        embeddings.append(emb)

        # upload in batches to avoid huge payloads (Chroma accepts batch inserts)

        if len(ids) >= batch_size:

            collection.add(

                ids=ids,

                documents=documents,

                metadatas=metadatas,

                embeddings=embeddings

            )

            ids, documents, metadatas, embeddings = [], [], [], []

    # final batch

    if ids:

        collection.add(ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings)

    # persist to disk

    # persist()

    logger.info("Upload finished. Skipped %d records.", skipped)

    return True
 



 