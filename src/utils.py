from src.schema.output_schema import SQLTableSchema
from typing import Any

relationships = {
    "address": {
        "city": "address.city_id -> city.city_id"
    },
    "city": {
        "country": "city.country_id -> country.country_id"
    },
    "customer": {
        "address": "customer.address_id -> address.address_id",
        "store": "customer.store_id -> store.store_id"
    },
    "film": {
        "language": "film.language_id -> language.language_id"
    },
    "film_actor": {
        "film": "film_actor.film_id -> film.film_id",
        "actor": "film_actor.actor_id -> actor.actor_id"
    },
    "film_category": {
        "category": "film_category.category_id -> category.category_id",
        "film": "film_category.film_id -> film.film_id"
    },
    "inventory": {
        "film": "inventory.film_id -> film.film_id",
        "store": "inventory.store_id -> store.store_id"
    },
    "payment": {
        "customer": "payment.customer_id -> customer.customer_id"
    },
    "rental": {
        "customer": "rental.customer_id -> customer.customer_id"
    },
    "staff": {
        "address": "staff.address_id -> address.address_id"
    },
    "store": {
        "address": "store.address_id -> address.address_id"
    }
}

def get_schema_prompt(schema_results: list[dict[str,Any]]) -> str:
    blocks = []
    included_tables = {result["payload"]["table"] for result in schema_results}

    for result in schema_results:
        table = result["payload"]["table"]
        description = result["payload"]["description"]
        ddl = result["payload"]["ddl"]

        block = f"{ddl}"
        blocks.append(block)

    rel_lines = []
    for table, rels in relationships.items():
        if table in included_tables:
            for rel in rels.values():
                left, right = rel.split("->")
                left_table = left.strip().split(".")[0]
                right_table = right.strip().split(".")[0]
                if left_table in included_tables and right_table in included_tables:
                    rel_lines.append(f"- {rel}")

    rel_block = ""
    if rel_lines:
        rel_block = "\n\n### Relationships\n" + "\n".join(rel_lines)

    return "\n\n".join(blocks) + rel_block


def format_pseudo_schema(question: str, pseudo_schema: SQLTableSchema) -> tuple[str, int]:
    ddl_block = " ".join(pseudo_schema.create_statements)
    ddl = f"Question: {question} {ddl_block}"
    count = len(pseudo_schema.create_statements)
    return ddl, count

