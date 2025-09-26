from sqlalchemy import create_engine
from src.config import config

engine = create_engine(f"postgresql://{config.postgres_name}:{config.postgres_pass}@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}")
