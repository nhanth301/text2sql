from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult
from src.node.pseudo_sql import pseudo_sql_node
from src.node.pseudo_schema import pseudo_schema_node
from src.node.schema_retrieval import schema_retrieval_node
from src.node.fix_sql import fix_sql_node
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm

QUESTION= 'List the top 5 films with the highest number of rentals in 2022'


def test():
    result = pseudo_sql_node(gemini_llm,QUESTION)
    assert isinstance(result, SQLGenerationSchema)
    assert not result.sql.strip().startswith("```")
    assert "SELECT" in result.sql.upper()



