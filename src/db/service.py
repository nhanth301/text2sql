from src.db.client import engine
from src.schema.output_schema import QueryResponse, SQLGenerationSchema
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

def query(sql_query: SQLGenerationSchema, return_dict: bool = False) -> QueryResponse | dict :
    try:
        result = pd.read_sql(sql_query.sql, engine)
        if return_dict:
            result = result.to_dict()
        return QueryResponse(result=result, error=None)
    except SQLAlchemyError as e:
        return QueryResponse(result=None, error=str(e.__cause__ or e)) if not return_dict else {'error': str(e.__cause__ or e)}
    except Exception as e:
        return QueryResponse(result=None, error=str(e)) if not return_dict else {'error': str(e)}

