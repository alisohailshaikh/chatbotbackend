#main page to get find multi model pdf embeddings project
import streamlit as st
from dotenv import load_dotenv

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with Multiple PDFS", page_icon=":soccer:", layout="wide")
    #main header of the page
    st.header("Chat with Multiple PDFS :soccer:")
    st.text_input("Enter your question about your documents here: ")
    
    with st.sidebar:
        st.subheader("Your PDF Documents")
        st.file_uploader("Upload your PDF files here: ")
        st.button("Upload")

if __name__ == "__main__":
    main()