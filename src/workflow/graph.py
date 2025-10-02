from src.workflow.node import *
from src.schema.state_schema import InputState, OverallState, OutputState
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

builder = StateGraph(OverallState)
builder.add_node('add_message', add_message_node)
builder.add_node('intent_classifier', intent_llm_node)
builder.add_node('clarification_answer', intent_answer_node)

builder.add_node("pseudo_sql_generator", pseudo_sql_node)
builder.add_node("pseudo_schema_generator", pseudo_schema_node)
builder.add_node("schema_retriever", schema_retrieval_node)
builder.add_node("sql_generator", gen_sql_node)
builder.add_node("sql_validator", validate_sql_node)

builder.add_node("sql_fixer", fix_sql_node)
builder.add_node("sql_executor", execute_sql_node)

builder.add_node("final_answer_generator", sql_answer_node)
builder.add_node("break_answer", break_answer_node)

builder.add_edge(START, 'add_message')
builder.add_edge("add_message", "intent_classifier")

builder.add_conditional_edges(
    "intent_classifier",
    intent_router,
    {
        "CONTINUE": "pseudo_sql_generator",
        "END": "clarification_answer"
    }
)

builder.add_edge("pseudo_sql_generator", "pseudo_schema_generator")
builder.add_edge("pseudo_schema_generator", "schema_retriever")
builder.add_edge("schema_retriever", "sql_generator")
builder.add_edge("sql_generator", "sql_validator")

builder.add_conditional_edges(
    "sql_validator",
    sql_validation_router,
    {
        "CONTINUE": "sql_executor",
        "FIX": "sql_fixer",
        'END': "break_answer"
    }
)

builder.add_conditional_edges(
    "sql_executor",
    sql_execution_router,
    {
        "CONTINUE": "final_answer_generator",
        "FIX": "sql_fixer"
    }
)
builder.add_edge("sql_fixer", "sql_validator")

builder.add_edge("final_answer_generator", END)
builder.add_edge("clarification_answer", END)

graph = builder.compile(checkpointer=checkpointer)

# print(graph.invoke({'user_question': 'Show the name of each film with its category'}, {"configurable": {"thread_id": "2"}}))   

