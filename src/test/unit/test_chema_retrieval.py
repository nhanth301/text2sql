from src.node.schema_retrieval import schema_retrieval_node
from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult

SCHEMA = SQLTableSchema(create_statements=['CREATE TABLE stores (store_id INTEGER PRIMARY KEY, customer_id INTEGER);', 
                                           'CREATE TABLE customers (customer_id INTEGER PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), address_id INTEGER'])

def test():
    result = schema_retrieval_node(pseudo_schema=SCHEMA,k=2)
    assert isinstance(result,str)

