from src.vectordb.service import search, se_search
from src.db.service import query
from src.llm.client import llm, vip_llm, pro_llm
from src.llm.prompt import SYSTEM_PROMPT, PSEUDO_SQL_GEN_PROMPT, PSEUDO_SCHEMA_GEN_PROMPT, FIX_SQL_PROMPT
from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema
from src.utils import get_schema_prompt, format_pseudo_schema
def main():


    question = 'List the top 5 films with the highest number of rentals in 2022'
    sql_chain = PSEUDO_SQL_GEN_PROMPT | pro_llm.with_structured_output(SQLGenerationSchema)
    sql_result = sql_chain.invoke({'question': question})
    print(sql_result.sql)
    print("pseudo sql")

    pseudo_schema_chain = PSEUDO_SCHEMA_GEN_PROMPT | vip_llm.with_structured_output(SQLTableSchema)
    pseudo_schema_result = pseudo_schema_chain.invoke({'sql': sql_result.sql})

    print(pseudo_schema_result)
    print("pseudo schema")
    

    schema = se_search(pseudo_schema_result)
    schema = get_schema_prompt(schema)
    print(schema)
    print("retrieval schema")


    chain = SYSTEM_PROMPT | llm.with_structured_output(SQLGenerationSchema)
    result = chain.invoke({'question': question, 'schema': schema})
    print(result)
    print("########")

    response = query(result.sql)
    
    if response.error:
        print("###SQL error:", response.error)
        error_chain = FIX_SQL_PROMPT | llm.with_structured_output(SQLGenerationSchema)
        fix_result = error_chain.invoke({'question': question, 'query': result.sql, 'schema': schema, 'error': response.error})
        print(fix_result.sql)
        fix_sql_response = query(fix_result.sql)
        print(fix_sql_response)
    else:
        print("Result:", response.result)


                        

if __name__ == '__main__':
    main()


