from src.db.client import engine
import pandas as pd

def query(sql_query: str, return_dict = False) -> dict:
    result = pd.read_sql(sql_query, engine)
    return result.to_dict() if return_dict else result
