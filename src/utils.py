

def get_schema_prompt(schema_results: dict[str]) -> str:
    return "\n".join([f"Table: {result['payload']['table']}\nDescription: {result['payload']['description']}\nSchema: {result['payload']['ddl']}" for result in schema_results])