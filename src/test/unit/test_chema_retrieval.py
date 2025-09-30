from src.component.schema_retrieval import schema_retrieval
from src.schema.output_schema import SQLTableSchema

SCHEMA = SQLTableSchema(create_statements=['CREATE TABLE stores (store_id INTEGER PRIMARY KEY, customer_id INTEGER);', 
                                           'CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), address_id INTEGER'])

def test():
    result = schema_retrieval(pseudo_schema=SCHEMA,k=2)
    assert isinstance(result[0],list)
    assert isinstance(result[1],str)

