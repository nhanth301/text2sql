from pydantic import BaseModel
from pandas import DataFrame
from src.schema.output_schema import SQLGenerationSchema, SQLTableSchema, SQLValidationResult, QueryResponse
from typing import Any, Annotated, TypedDict

MAX_HISTORY = 6
def recent_messages_reducer(left: list[str], right: list[str]) -> list[str]:
    merged = (left or []) + (right or [])
    return merged[-MAX_HISTORY:]


class InputState(TypedDict):
    pass
    
class OutputState(TypedDict):
    pass

class OverallState(TypedDict):
    user_question: str  

    recent_messages: Annotated[list[str], recent_messages_reducer]
    intent: str | None
    pseudo_sql: SQLGenerationSchema 
    pseudo_schema: SQLTableSchema 
    retrieved_schema: list[dict[str,Any]] 
    schema_prompt: str 
    sql: SQLGenerationSchema 
    sql_validation_result: SQLValidationResult 
    sql_execution_result: QueryResponse
    
    valid_count: int

    table_result: Any
    answer: str | None








