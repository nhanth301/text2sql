from src.component.schema_retrieval import schema_retrieval
from src.schema.output_schema import SQLTableSchema

SCHEMA = SQLTableSchema(create_statements=['CREATE TABLE film (film_id INTEGER PRIMARY KEY, title VARCHAR(255));'])

def test():
    result = schema_retrieval("show the name and category of each film",pseudo_schema=SCHEMA,k=5)
    for r in result[0]:
        print(r['payload']['ddl'])
    assert isinstance(result[0],list)
    assert isinstance(result[1],str)