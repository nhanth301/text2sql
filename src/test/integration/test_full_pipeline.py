import pytest
from src.component.pseudo_sql import pseudo_sql
from src.component.pseudo_schema import pseudo_schema
from src.component.schema_retrieval import schema_retrieval
from src.component.gen_sql import gen_sql
from src.component.validate_sql import validate_sql
from src.component.fix_sql import fix_sql
from src.component.execute_sql import execute_sql
from src.llm.client import gemini_llm
from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult, QueryResponse

QUESTION = "List the top 5 films with the highest number of rentals in 2022"

def test_full_pipeline():
    sql_guess = pseudo_sql(gemini_llm, QUESTION)
    assert isinstance(sql_guess, SQLGenerationSchema)

    inferred_schema = pseudo_schema(gemini_llm, sql_guess)
    assert isinstance(inferred_schema, SQLTableSchema)

    retrieved_schema, _ = schema_retrieval(
        QUESTION,
        pseudo_schema=inferred_schema,
        k=5
    )
    assert isinstance(retrieved_schema, list)
    schema_str = "\n".join([r["payload"]["ddl"] for r in retrieved_schema])

    sql_final = gen_sql(
        llm=gemini_llm,
        question=QUESTION,
        schema=schema_str
    )
    assert isinstance(sql_final, SQLGenerationSchema)

    validation = validate_sql(
        llm=gemini_llm,
        question=QUESTION,
        sql=sql_final,
        schema=schema_str
    )
    assert isinstance(validation, SQLValidationResult)

    if not validation.is_valid:
        fixed_sql = fix_sql(
            llm=gemini_llm,
            valid=validation,
            question=QUESTION,
            schema=schema_str,
            error_sql=sql_final
        )
        assert isinstance(fixed_sql, SQLGenerationSchema)
        sql_to_run = fixed_sql
    else:
        sql_to_run = sql_final

    result = execute_sql(sql=sql_to_run, return_dict=True)
    assert isinstance(result, dict) or isinstance(result, QueryResponse)
