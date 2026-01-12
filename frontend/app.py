# app.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
from backend.blob_utils import load_schema_from_blob
from backend.index_manager import create_collection_if_not_exists, upload_schema_to_collection
from backend.retrieval import retrieve_relevant_schema_chroma
from backend.sql_generator import generate_sql
def main():
    st.set_page_config(page_title="QNXT SQL Chatbot")
    st.title("🔍 AI Chatbot for QNXT Schema – SQL Query Generator")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "schema_json" not in st.session_state:
        st.session_state.schema_json = None
    st.sidebar.header("🛠️ Tools & Actions")
    if st.sidebar.button("🗃️ Rebuild Index"):
        with st.spinner("Creating schema embeddings into ChromaDB..."):
            try:
                create_collection_if_not_exists()
                schema_json = load_schema_from_blob()
                if not schema_json:
                    st.sidebar.error("Failed to fetch schema.")
                else:
                    st.session_state.schema_json = schema_json
                    upload_schema_to_collection(schema_json)
                    st.sidebar.success("Schema uploaded into ChromaDB.")
            except Exception as e:
                st.sidebar.error(f"Indexing failed: {e}")
    if st.sidebar.button("🧹 Clear Conversation"):
        st.session_state.chat_history = []
        st.sidebar.success("Conversation history cleared.")
    user_input = st.chat_input("Type your query in natural language...")
    if user_input:
        with st.spinner("Retrieving schema and generating SQL query..."):
            try:
                schema_to_use = st.session_state.schema_json or load_schema_from_blob()
                relevant_schema = retrieve_relevant_schema_chroma(user_input, top_k=5)
                sql_query = generate_sql(relevant_schema, user_input, st.session_state.chat_history)
            except Exception as e:
                st.error(f"Error: {e}")
                sql_query = f"-- Error generating query: {e}"
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": sql_query})
    st.subheader("🗨️ Conversation History")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.code(msg["content"], language="sql")
            else:
                st.markdown(msg["content"])
if __name__ == "__main__":
    main()
 







 