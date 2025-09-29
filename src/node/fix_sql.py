from src.schema.output_schema import SQLGenerationSchema, SQLValidationResult
from src.llm.prompt import FIX_SQL_PROMPT
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

def fix_sql_node(llm: ChatOllama | ChatGoogleGenerativeAI,
                 valid: SQLValidationResult,
                 question: str,
                 schema: str,
                 error_sql: SQLGenerationSchema):
    try:
        chain = FIX_SQL_PROMPT | llm.with_structured_output(SQLGenerationSchema)
        chain_result = chain.invoke({
            'question': question,
            'schema': schema,
            'error_sql': error_sql.sql,
            'error': ','.join(valid.errors)
        })
        return chain_result
    except Exception as e:
        raise e 