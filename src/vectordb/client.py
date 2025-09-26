from qdrant_client import QdrantClient
from src.config import config

client = QdrantClient(
    url=config.qdrant_host,
    port=config.qdrant_port
)