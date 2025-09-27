from pydantic import BaseModel, Field, field_validator

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
