import chainlit as cl
import pandas as pd
from src.workflow.graph import graph 

async def run_langgraph_workflow(user_input: str):
    thread_id = cl.user_session.get("id") 
    
    response = await cl.make_async(graph.invoke)(
        {"user_question": user_input},
        {"configurable": {"thread_id": thread_id}}
    )
    return response

@cl.on_message 
async def main(message: cl.Message):
    response = await run_langgraph_workflow(message.content)

    answer = response.get('answer', "Sorry, I couldn't process that.")
    table_result = response.get('table_result')

    elements = []
    if table_result is not None:

        df = pd.DataFrame(table_result)
        print(df)
        if not df.empty:
            elements.append(
                cl.Dataframe(data=df, name="Query Result")
            )

    await cl.Message(
        content=answer,
        elements=elements,
    ).send()

@cl.on_chat_start
async def start():
    await cl.Message(
        content="## 🤖 Hi, I'm the Database Assistant!\n\nAsk me anything about your data...",
    ).send()