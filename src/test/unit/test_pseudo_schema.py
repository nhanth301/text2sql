from src.component.pseudo_schema import pseudo_schema
from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm

SQL = SQLGenerationSchema(sql="""
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id;
""")

def test():
    result = pseudo_schema(gemini_llm, SQL)
    assert isinstance(result, SQLTableSchema)
    assert all("CREATE TABLE" in r.upper() for r in result.create_statements)