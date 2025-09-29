from src.vectordb.service import se_search
from src.utils import get_schema_prompt
from src.schema.output_schema import SQLTableSchema


def schema_retrieval_node(pseudo_schema: SQLTableSchema, k: int = 2) -> str:
    try:
        result = se_search(tables=pseudo_schema,k=k)
        prompt = get_schema_prompt(result)
        return prompt
    except Exception as e:
        raise e
    