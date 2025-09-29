from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from src.llm.prompt import PSEUDO_SCHEMA_GEN_PROMPT

def pseudo_schema_node(llm: ChatOllama | ChatGoogleGenerativeAI, pseudo_sql: SQLGenerationSchema) -> SQLTableSchema:
    try:
        chain = PSEUDO_SCHEMA_GEN_PROMPT | llm.with_structured_output(SQLTableSchema)
        chain_result = chain.invoke({'sql': pseudo_sql.sql})
        return chain_result
    except Exception as e:
        raise e 
