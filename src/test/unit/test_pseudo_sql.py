from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult
from src.component.pseudo_sql import pseudo_sql
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm

QUESTION= 'List the top 5 films with the highest number of rentals in 2022'


def test():
    result = pseudo_sql(gemini_llm,QUESTION)
    assert isinstance(result, SQLGenerationSchema)
    assert not result.sql.strip().startswith("```")
    assert "SELECT" in result.sql.upper()



