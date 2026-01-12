# backend/retrieval.py

from typing import List

from backend.chroma_client import get_or_create_collection, get_client

from backend.embeddings import generate_embedding

from backend import config

from backend.azure_clients import logger

from backend.index_manager import EMBED_DIM  # re-use constant

import numpy as np

COLLECTION_NAME = getattr(config, "INDEX_NAME", "qnxt-schema-collection")

def _format_columns_for_display(cols):

    if not cols:

        return ""

    if isinstance(cols, list):

        parts = []

        for c in cols:

            name = c.get("name") or ""

            dtype = c.get("datatype") or ""

            cdesc = c.get("column_description") or ""

            parts.append(f"{name} ({dtype}) - {cdesc}" if name else f"{cdesc}")

        return "; ".join(parts)

    return str(cols)

def retrieve_relevant_schema_chroma(user_input: str, top_k: int = 5) -> str:

    """

    Query Chroma using vector similarity. Returns formatted string lines like:

      Table: <tableName>, Description: <...>, Columns: <...>

    """

    # compute embedding

    try:

        q_emb = generate_embedding(user_input)

    except Exception as e:

        logger.exception("Failed to create embedding for query: %s", e)

        return ""

    if not isinstance(q_emb, list) or len(q_emb) != EMBED_DIM:

        logger.warning("Query embedding shape unexpected.")

        return ""

    coll = get_or_create_collection(COLLECTION_NAME)

    # Chroma query

    try:

        results = coll.query(

            query_embeddings=[q_emb],

            n_results=top_k,

            include=["metadatas", "documents", "distances"]

        )

    except Exception as e:

        logger.exception("Chroma query failed: %s", e)

        return ""

    # results is dict; extract first (single query)

    metas = results.get("metadatas", [[]])[0]

    docs = results.get("documents", [[]])[0]

    ids = results.get("ids", [[]])[0]

    dists = results.get("distances", [[]])[0]

    lines = []

    for md, doc, _id, dist in zip(metas, docs, ids, dists):

        table_name = md.get("tableName") or _id

        tdesc = md.get("table_description") or md.get("description") or (doc[:300] if doc else "")

        cols = md.get("columns") or []

        cols_str = _format_columns_for_display(cols)

        lines.append(f"Table: {table_name}, Description: {tdesc}" + (f", Columns: {cols_str}" if cols_str else ""))

    # If nothing returned, fallback to simple keyword scan over all docs

    if not lines:

        # fallback: scan all documents in collection for substring matches (cheap for dev)

        try:

            all_docs = coll.get(include=["metadatas", "documents", "ids"])

            docs_all = all_docs.get("documents", [])

            metas_all = all_docs.get("metadatas", [])

            ids_all = all_docs.get("ids", [])

            hits = []

            q_lower = user_input.lower()

            for md, doc, _id in zip(metas_all, docs_all, ids_all):

                if q_lower in (doc or "").lower():

                    table_name = md.get("tableName") or _id

                    tdesc = md.get("table_description") or ""

                    cols_str = _format_columns_for_display(md.get("columns") or [])

                    hits.append(f"Table: {table_name}, Description: {tdesc}" + (f", Columns: {cols_str}" if cols_str else ""))

                    if len(hits) >= top_k:

                        break

            return "\n".join(hits)

        except Exception:

            logger.exception("Chroma fallback scan failed.")

            return ""

    return "\n".join(lines)
 