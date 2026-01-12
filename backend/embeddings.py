# embeddings.py
import openai
from backend import config
def generate_embedding(text: str):
    """
    Produce an embedding via Azure OpenAI embedding deployment specified in config.
    """
    resp = openai.Embedding.create(engine=config.EMBEDDING_DEPLOYMENT, input=text)
    return resp["data"][0]["embedding"]