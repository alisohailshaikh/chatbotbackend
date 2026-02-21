from langchain_community.memory import ConversationBufferMemory
from langchain_community.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    llm = ChatOpenAI()
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    return conversation_chain
    