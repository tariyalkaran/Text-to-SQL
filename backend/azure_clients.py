# azure_clients.py
import openai
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from backend import config
import logging

# configure OpenAI global settings (Azure OpenAI)
openai.api_type = config.OPENAI_API_TYPE
openai.api_base = config.OPENAI_API_BASE
openai.api_version = config.OPENAI_API_VERSION
openai.api_key = config.OPENAI_API_KEY

# Blob client
blob_service_client = BlobServiceClient.from_connection_string(config.AZURE_STORAGE_CONNECTION_STRING)


# basic logger for modules
logger = logging.getLogger("qnxt_sql_chatbot")
logger.setLevel(logging.INFO)