from src.component.schema_retrieval import schema_retrieval
from src.component.execute_sql import execute_sql
from src.component.fix_sql import fix_sql
from src.component.gen_sql import gen_sql
from src.component.pseudo_schema import pseudo_schema
from src.component.pseudo_sql import pseudo_sql
from src.component.validate_sql import validate_sql
from src.llm.client import gemini_llm, creative_gemini_llm
from src.llm.prompt import INTENT_PROMPT
from src.schema.state_schema import OverallState
from src.schema.output_schema import IntentSchema, SQLValidationResult
from langchain_core.messages import AIMessage, HumanMessage
from src.logging import logger


def add_message_node(state: OverallState) -> OverallState:
    logger.info("Node: add_message_node")
    logger.debug(f"Adding user question to history: '{state['user_question']}'")
    return {'recent_messages': [HumanMessage(content=state['user_question'])], 'valid_count': 0}


def intent_llm_node(state: OverallState) -> OverallState:
    logger.info("Node: intent_llm_node")
    history = "\n".join([f"{m.type.upper()}: {m.content}" for m in state["recent_messages"]])
    logger.debug(f"History for intent detection:\n{history}")

    intent_parser = INTENT_PROMPT | creative_gemini_llm.with_structured_output(IntentSchema)
    result = intent_parser.invoke({"history": history})

    logger.info(f"Intent detection result: {result}")
    return {
        "intent": result.intent,
        "recent_messages": [AIMessage(content=result.clarification)]
        if result.intent is None and result.clarification else []
    }


def intent_router(state: OverallState) -> str:
    logger.info("Router: intent_router")
    intent = state.get('intent')
    logger.debug(f"Checking intent: '{intent}'")
    if intent:
        logger.info("Decision: CONTINUE to SQL generation flow.")
        return 'CONTINUE'
    logger.warning("Decision: END with clarification.")
    return 'END'


def pseudo_sql_node(state: OverallState) -> OverallState:
    logger.info("Node: pseudo_sql_node")
    user_intent = state['intent']
    logger.debug(f"Generating pseudo SQL for intent: '{user_intent}'")

    result = pseudo_sql(llm=gemini_llm, question=user_intent)
    logger.debug(f"Generated Pseudo SQL: {result}")

    return {'pseudo_sql': result, 'intent': user_intent}


def pseudo_schema_node(state: OverallState) -> OverallState:
    logger.info("Node: pseudo_schema_node")
    pseudo_sql_val = state['pseudo_sql']
    logger.debug(f"Generating pseudo schema from pseudo SQL: {pseudo_sql_val}")

    result = pseudo_schema(llm=gemini_llm, pseudo_sql=pseudo_sql_val)
    logger.debug(f"Generated Pseudo Schema: {result}")

    return {'pseudo_schema': result}


def schema_retrieval_node(state: OverallState) -> OverallState:
    logger.info("Node: schema_retrieval_node")
    pseudo_schema_val = state['pseudo_schema']
    logger.debug(f"Retrieving schema based on pseudo schema: {pseudo_schema_val}")

    schema_result, prompt_result = schema_retrieval(
        question=state['intent'], pseudo_schema=pseudo_schema_val, k=1
    )
    logger.debug(f"Schema prompt:\n{prompt_result}")
    logger.info(f"Retrieved {len(schema_result)} tables.")

    return {'retrieved_schema': schema_result, 'schema_prompt': prompt_result}


def gen_sql_node(state: OverallState) -> OverallState:
    logger.info("Node: gen_sql_node")
    question = state['intent']
    logger.debug(f"Generating final SQL for question: '{question}'")

    result = gen_sql(llm=gemini_llm, question=question, schema=state['schema_prompt'])
    logger.debug(f"Generated SQL: {result.sql}")

    return {'sql': result}


def validate_sql_node(state: OverallState) -> OverallState:
    logger.info("Node: validate_sql_node")
    sql = state['sql']
    logger.debug(f"Validating SQL: {sql.sql}")

    result = validate_sql(
        llm=gemini_llm, question=state['intent'], sql=sql, schema=state['schema_prompt']
    )
    logger.info(f"Validation result: is_valid={result.is_valid}, errors={result.errors}")

    return {'sql_validation_result': result, 'valid_count': state['valid_count'] + 1}


def sql_validation_router(state: OverallState) -> str:
    logger.info("Router: sql_validation_router")
    validation = state['sql_validation_result']
    logger.debug(f"Checking validation result: is_valid={validation.is_valid}")

    if validation.is_valid:
        logger.info("Decision: CONTINUE to execution.")
        return "CONTINUE"

    if state['valid_count'] <= 3:
        logger.warning("Decision: FIX SQL.")
        return "FIX"
    return "END"


def fix_sql_node(state: OverallState) -> OverallState:
    logger.info("Node: fix_sql_node")
    sql = state['sql']
    validation = state['sql_validation_result']
    logger.warning(f"Attempting to fix SQL due to errors: {validation.errors}")

    result = fix_sql(
        llm=gemini_llm,
        valid=validation,
        question=state['intent'],
        schema=state['schema_prompt'],
        error_sql=sql,
    )
    logger.debug(f"New fixed SQL: {result.sql}")

    return {'sql': result}


def execute_sql_node(state: OverallState) -> OverallState:
    logger.info("Node: execute_sql_node")
    sql = state['sql']
    logger.debug(f"Executing SQL: {sql.sql}")

    result = execute_sql(sql=sql, return_dict=True)
    if result.error:
        logger.error(f"Execution FAILED. Error: {result.error}")
    else:
        logger.info(f"Execution SUCCEEDED. Result preview: {str(result.result)[:200]}...")

    validation = SQLValidationResult(
        is_valid=result.error is None,
        errors=[result.error] if result.error else []
    )
    return {'sql_execution_result': result, 'sql_validation_result': validation}


def sql_execution_router(state: OverallState) -> str:
    logger.info("Router: sql_execution_router")
    execution_result = state['sql_execution_result']
    has_error = execution_result.error is not None
    logger.debug(f"Checking execution result: has_error={has_error}")

    if has_error:
        logger.warning("Decision: FIX SQL due to execution error.")
        return "FIX"

    logger.info("Decision: CONTINUE to final answer.")
    return "CONTINUE"


def sql_answer_node(state: OverallState) -> OverallState:
    logger.info("Node: sql_answer_node")
    result = state['sql_execution_result']
    data = result.result

    import pandas as pd
    ai_message = pd.DataFrame(data).head(3).to_dict()
    logger.debug(f"Answer preview (first 3 rows): {ai_message}")

    logger.info("Generating final answer for the user.")
    return {
        'table_result': data,
        'answer': 'Here you are!!',
        'recent_messages': [AIMessage(content="[SQL_RESULT]:" + str(ai_message))]
    }


def intent_answer_node(state: OverallState) -> OverallState:
    logger.info("Node: intent_answer_node")
    clarification = state['recent_messages'][-1]
    logger.debug(f"Returning clarification question: '{clarification}'")
    return {'answer': clarification.content, 'table_result': None}

def break_answer_node(state: OverallState) -> OverallState:
    logger.info("Node: break_answer_node")
    return {'answer': "Sorry, i can't help", 'table_result': None}

