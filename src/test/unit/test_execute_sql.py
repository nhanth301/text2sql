from src.component.execute_sql import execute_sql
from src.schema.output_schema import QueryResponse, SQLGenerationSchema

SQL = SQLGenerationSchema(sql="""
SELECT f.title, c.name
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category c ON fc.category_id = c.category_id;
""")

def test():
    result = execute_sql(sql=SQL,return_dict=False)
    assert isinstance(result, QueryResponse)
    result = execute_sql(sql=SQL,return_dict=True)
    assert isinstance(result, dict)