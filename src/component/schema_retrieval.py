from src.vectordb.service import se_search
from src.utils import get_schema_prompt
from src.schema.output_schema import SQLTableSchema
from typing import Any

def schema_retrieval(pseudo_schema: SQLTableSchema, k: int = 2) -> tuple[list[dict[str,Any]],str]:
    try:
        result = se_search(tables=pseudo_schema,k=k)
        prompt = get_schema_prompt(result)
        return result, prompt
    except Exception as e:
        raise e
    