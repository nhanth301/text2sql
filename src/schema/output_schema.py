from pydantic import BaseModel, Field, field_validator
from typing import Optional, Any


class SQLGenerationSchema(BaseModel):
    sql: str = Field(..., description="The generated SQL statement (must not include ```sql fences)")

    @field_validator("sql")
    def not_wrap_with_codeblock(cls, v: str):
        if v.strip().startswith("```"):
            parts = v.strip().split("```")
            for p in parts:
                if p.strip().lower().startswith("sql"):
                    cleaned = p.strip()[3:].strip()
                    if cleaned:
                        return cleaned
            return v.replace("```", "").strip()
        return v

class SQLValidationResult(BaseModel):
    is_valid: bool = Field(
        ...,
        description="True if the generated SQL is valid against the schema, False otherwise"
    )
    errors: list[str] = Field(
        default_factory=list,
        description="List of problems found with the SQL, empty if none"
    )


class SQLTableSchema(BaseModel):
    create_statements: list[str] = Field(
        ...,
        description="List of CREATE TABLE statements in PostgreSQL syntax for the inferred schema"
    )

class QueryResponse(BaseModel):
    result: Optional[Any] = Field(
        None, description="Query result, either a DataFrame-like dict or other serializable structure."
    )
    error: Optional[str] = Field(
        None, description="Error message if the query failed."
    )