from src.schema.output_schema import SQLGenerationSchema
from src.llm.prompt import SQL_GEN_PROMPT
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI

def gen_sql(llm: ChatOllama | ChatGoogleGenerativeAI, question: str, schema: str) -> SQLGenerationSchema:
    chain = SQL_GEN_PROMPT | llm.with_structured_output(SQLGenerationSchema)
    try:
        chain_result = chain.invoke({'question': question, 'schema': schema})
        return chain_result
    except Exception as e:
        raise e