from src.db.service import query
from src.schema.output_schema import QueryResponse, SQLGenerationSchema

def execute_sql(sql: SQLGenerationSchema, return_dict: bool = False) -> QueryResponse | dict:
    response = query(sql,return_dict)
    return response

    