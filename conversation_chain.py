from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory


def get_conversation_chain(vectorstore):

    llm = ChatOpenAI(model="gpt-4o-mini")

    retriever = vectorstore.as_retriever()

    prompt = ChatPromptTemplate.from_template("""
    Answer the question based only on the context below.

    Context:
    {context}

    Chat History:
    {chat_history}

    Question:
    {input}
    """)

    # ✅ FIX: Extract only the string question for retriever
    def get_question(input_dict):
        return input_dict["input"]

    rag_chain = (
        {
            "context": RunnableLambda(get_question) | retriever,
            "input": RunnableLambda(get_question),
            "chat_history": RunnablePassthrough(),
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

    conversational_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
    )

    return conversational_chain