from src.component.fix_sql import fix_sql
from src.llm.client import gemini_llm, sqlcoder_llm, mistral_llm
from src.schema.output_schema import SQLGenerationSchema, SQLValidationResult

VALIDATION = SQLValidationResult(
    is_valid=False,
    errors=[
        "Column 'id' not found in table 'film' (did you mean 'film_id'?)",
        "Column 'id' not found in table 'film_category' (did you mean 'film_id' or 'category_id'?)",
        "Join condition is invalid: fc.id does not reference c.category_id"
    ]
)

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

ERROR_SQL = SQLGenerationSchema(sql="""
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.id = fc.id
JOIN category c ON fc.id = c.id;
""")

def test():
    result = fix_sql(llm=gemini_llm,
                          valid=VALIDATION,
                          question=QUESTION,
                          schema=SCHEMA,
                          error_sql=ERROR_SQL)
    assert isinstance(result, SQLGenerationSchema)
    assert not result.sql.strip().startswith("```")
    assert "SELECT" in result.sql.upper()