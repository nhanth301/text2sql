from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult
from src.component.validate_sql import validate_sql
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm


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

SQL = SQLGenerationSchema(sql="""
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id;
""")

ERROR_SQL = SQLGenerationSchema(sql="""
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.id = fc.id
JOIN category c ON fc.id = c.id;
""")

def test():
    #correct
    result = validate_sql(llm=gemini_llm,
                               question=QUESTION,
                               sql=SQL,
                               schema=SCHEMA)
    assert isinstance(result, SQLValidationResult)
    assert result.is_valid == True
    assert len(result.errors) == 0

    #wrong
    result = validate_sql(llm=gemini_llm,
                               question=QUESTION,
                               sql=ERROR_SQL,
                               schema=SCHEMA)
    assert isinstance(result, SQLValidationResult)
    assert result.is_valid == False
    assert len(result.errors) > 0


    