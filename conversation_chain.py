from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from retrieve_documents import retrieve_documents 
import os


def get_conversation_chain(user_id, document_id):

    llm = ChatOpenAI(model="gpt-4o-mini")

    USER_ID = user_id

    def get_context(input_dict):
        query = input_dict["input"]
        docs = retrieve_documents(query, USER_ID, document_id)
        if docs:
            return "\n".join(docs)
        return None
    
    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the context below.

    Context:
    {context}

    Chat History:
    {chat_history}

    Question:
    {input}
    """)

    chain = (
        {
            "context": RunnableLambda(get_context),
            "input": lambda x: x["input"],
            "chat_history": lambda x: x["chat_history"],
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    store = {}

    def get_session_history(session_id: str):
        if session_id not in store:
            store[session_id] = InMemoryChatMessageHistory()
        return store[session_id]

    return RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )