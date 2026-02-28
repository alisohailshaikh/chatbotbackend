#main page to get find multi model pdf embeddings project
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import get_pdf_text, get_text_chunks, get_vectorstore
from conversation_chain import get_conversation_chain


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFS", page_icon=":soccer:", layout="wide")
    #main header of the page
    st.header("Chat with Multiple PDFS :soccer:")  

    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    with st.sidebar:
        st.subheader("Your PDF Documents")
        pdf_docs = st.file_uploader("Upload your PDF files here: ", accept_multiple_files=True)
        if st.button("Upload"):
            if not pdf_docs:
                st.warning("Please upload at least one PDF.")
                return
            
            with st.spinner("Processing"):
                #get pdf text 
                raw_text = get_pdf_text(pdf_docs)

                #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                
                #create vector store
                vectorstore = get_vectorstore(text_chunks)

                #create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

    #CHAT INPUT
    user_question = st.chat_input("Ask a question about your documents")

    if user_question and st.session_state.conversation:

        response = st.session_state.conversation.invoke(
            {"input": user_question},
            config={"configurable": {"session_id": "streamlit_user"}}
        )

        st.session_state.chat_history.append(("user", user_question))
        st.session_state.chat_history.append(("assistant", response))
    else:
        st.info("Please upload your PDF documents to start the conversation.")
    #Display chat hsitory
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.write(message)

if __name__ == "__main__": 
    main()