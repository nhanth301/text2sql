from src.vectordb.service import search
from src.db.service import query
from src.llm.client import llm
from src.llm.prompt import SYSTEM_PROMPT
from src.schema.output_schema import SQLGenerationSchema
from src.utils import get_schema_prompt
def main():
    
    
    question = "List the top 10 films rented in 2022, showing the film title, category, total number of rentals, and the store where they were most frequently rented"
    schema_results = search(question,limit=8)
    schema = get_schema_prompt(schema_results)
    chain = SYSTEM_PROMPT | llm.with_structured_output(SQLGenerationSchema)
    result = chain.invoke({'question': question, 'schema': schema})
    print(query(result.sql))
                        

if __name__ == '__main__':
    main()


