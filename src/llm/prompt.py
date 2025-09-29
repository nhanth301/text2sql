from langchain.prompts import ChatPromptTemplate

SQL_GEN_PROMPT = ChatPromptTemplate.from_template(
    "You are a Text-to-SQL generator. "
    "The user will provide a natural language question and a database schema. "
    "Your task is to output ONLY the SQL query that correctly answers the question, "
    "using valid PostgreSQL syntax. "
    "Output must be the raw SQL query only.\n\n"
    "Schema:\n{schema}\n\nQuestion: {question}"
)

VALIDATE_SQL_PROMPT = ChatPromptTemplate.from_template("""
You are a SQL validation assistant.

Your task: check if the generated SQL query is valid given the provided schema and question.

Input:
- Question: {question}
- Schema: {schema}
- Generated SQL: {gen_sql}

Validation rules:
1. The SQL must only reference tables and columns that exist in the schema.
2. If a column or table is missing in the schema but appears in the SQL, it is invalid.
3. The SQL must be syntactically valid PostgreSQL.
4. The SQL must logically answer the question as best as possible with the given schema.

Output format (strict JSON):
{
  "is_valid": true/false,
  "errors": [list of problems found, empty if none]
}
""")



PSEUDO_SQL_GEN_PROMPT = ChatPromptTemplate.from_template("""
You are an assistant that converts a natural language question into a detailed SQL query.  
- Always output a single valid PostgreSQL SQL statement.  
- Do not include explanations, comments, or code fences.  
- Assume the database is fully normalized (3NF), so queries should involve multiple related tables.  
- Prefer queries with JOINs across different entities.  
- Even if the question could be answered with one table, expand it into a normalized multi-table query.  
- Use explicit JOIN syntax (INNER JOIN, LEFT JOIN, etc.).  
- Include GROUP BY, ORDER BY, and LIMIT when appropriate.  
- If your answer is not a valid JSON according to the schema, it will be discarded.
- Always wrap the response strictly as JSON matching the schema.                                                         
Question: {question}
""")

PSEUDO_SCHEMA_GEN_PROMPT = ChatPromptTemplate.from_template("""
You are given a SQL or pseudo-SQL query.  
Infer a possible relational database schema that would support this query.  

Instructions:
- Return only PostgreSQL CREATE TABLE statements.
- Each table must have a primary key if obvious.
- Add foreign keys when they can be inferred from the query.
- If something is not explicit, make a reasonable assumption (hallucination is acceptable).
- Do not add explanations, only CREATE TABLE statements.

SQL Query: {sql}
""")



FIX_SQL_PROMPT = ChatPromptTemplate.from_template("""
You are an expert SQL assistant. 
Your task is to fix invalid SQL queries based on the provided schema and error message.  

- Input includes:
  0. Natural question from user                                                
  1. The original SQL query (may be invalid).
  2. The database schema (DDL statements).
  3. The relationships between tables.
  4. The error message from the database.  

- You must output **only a corrected SQL query** that is valid for the given schema.  
- Do not include explanations, comments, or code fences.  
- Preserve the original intent of the query.  

- You must output **only a corrected SQL query** that is valid for the given schema.  
- Do not include explanations, comments, or code fences in your answer.  
- Keep the intent of the original query the same, only fix errors.  

Question:
{question}                                                  

Original Query:
{error_sql}

Schema:
{schema}

Error:
{error}

Corrected SQL:
""")