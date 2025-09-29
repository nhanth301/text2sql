from src.schema.output_schema import SQLGenerationSchema, SQLValidationResult
from src.llm.prompt import VALIDATE_SQL_PROMPT
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

def validate_sql_node(llm: ChatOllama | ChatGoogleGenerativeAI, 
                      question: str, 
                      sql: SQLGenerationSchema, 
                      schema: str) -> SQLValidationResult:
    try:
        chain = VALIDATE_SQL_PROMPT | llm.with_structured_output(SQLValidationResult)
        chain_result = chain.invoke({'question': question, 'gen_sql': sql, 'schema': schema})
        return chain_result
    except Exception as e:
        raise e 