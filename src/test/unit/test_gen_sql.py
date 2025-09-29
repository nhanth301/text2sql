from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm
from src.node.gen_sql import gen_sql_node

QUESTION= 'Show each film with its category'
SCHEMA = """
CREATE TABLE film (
    film_id SERIAL PRIMARY KEY,
    title TEXT
);

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE film_category (
    film_id INT REFERENCES film(film_id),
    category_id INT REFERENCES category(category_id)
);
"""
def test():
    result = gen_sql_node(llm=gemini_llm,
                          question=QUESTION,
                          schema=SCHEMA)
    assert isinstance(result, SQLGenerationSchema)
    assert not result.sql.strip().startswith("```")
    assert "SELECT" in result.sql.upper()
