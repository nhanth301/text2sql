from dataclasses import dataclass

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


config = Config(qdrant_host='localhost',
                qdrant_port='6333',
                qdrant_collection='db_schema',
                dense_vector_name='dense',
                sparse_vector_name='sparse',
                embedding_model_name='BAAI/bge-m3',
                postgres_host='localhost',
                postgres_port='5432',
                postgres_name='postgres',
                postgres_pass='admin',
                postgres_db='pagila')
