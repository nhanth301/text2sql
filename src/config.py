from dataclasses import dataclass
from dotenv import load_dotenv
import os 
load_dotenv()

@dataclass
class Config:
    qdrant_host: str
    qdrant_port: str
    qdrant_collection: str 
    dense_vector_name: str 
    sparse_vector_name: str | None
    embedding_model_name: str

    postgres_host: str
    postgres_port: str
    postgres_name: str 
    postgres_pass: str 
    postgres_db: str

    google_api_key: str
    together_api_key: str


config = Config(
    qdrant_host=os.getenv("QDRANT_HOST"),
    qdrant_port=os.getenv("QDRANT_PORT"),
    qdrant_collection=os.getenv("QDRANT_COLLECTION"),
    dense_vector_name=os.getenv("DENSE_VECTOR_NAME"),
    sparse_vector_name=os.getenv("SPARSE_VECTOR_NAME"), 
    embedding_model_name=os.getenv("EMBEDDING_MODEL_NAME"),

    postgres_host=os.getenv("POSTGRES_HOST"),
    postgres_port=os.getenv("POSTGRES_PORT"),
    postgres_name=os.getenv("POSTGRES_NAME"),
    postgres_pass=os.getenv("POSTGRES_PASS"),
    postgres_db=os.getenv("POSTGRES_DB"),
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    together_api_key=os.getenv("TOGETHER_API_KEY")
)