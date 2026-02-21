#main page to get find multi model pdf embeddings project
import streamlit as st
from dotenv import load_dotenv
from pdf_utils import get_pdf_text, get_text_chunks, get_vectorstore


def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFS", page_icon=":soccer:", layout="wide")
    #main header of the page
    st.header("Chat with Multiple PDFS :soccer:")
    st.text_input("Enter your question about your documents here: ")
    
    with st.sidebar:
        st.subheader("Your PDF Documents")
        pdf_docs = st.file_uploader("Upload your PDF files here: ", accept_multiple_files=True)
        if st.button("Upload"):
            with st.spinner("Processing"):
                #get pdf text 
                raw_text = get_pdf_text(pdf_docs)

                #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                
                #create vector store
                vectorstore = get_vectorstore(text_chunks)


if __name__ == "__main__": 
    main()