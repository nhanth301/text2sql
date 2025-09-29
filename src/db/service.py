from src.db.client import engine
from src.schema.output_schema import QueryResponse
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

def query(sql_query: str, return_dict: bool = False) -> QueryResponse:
    try:
        result = pd.read_sql(sql_query, engine)
        if return_dict:
            result = result.to_dict()
        return QueryResponse(result=result, error=None)
    except SQLAlchemyError as e:
        return QueryResponse(result=None, error=str(e.__cause__ or e))
    except Exception as e:
        return QueryResponse(result=None, error=str(e))

