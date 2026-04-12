# #main page to get find multi model pdf embeddings project
# from tabnanny import check

# import streamlit as st
# from dotenv import load_dotenv
# load_dotenv()
# from pdf_utils import get_pdf_text, get_text_chunks, get_vectorstore
# from conversation_chain import get_conversation_chain
# from check_for_documents import has_documents_for_user
# from auth import sign_up, sign_in, sign_out


# def main():
#     if "user" not in st.session_state:
#         st.session_state.user = None
#         if st.session_state.user is None:

#             st.title("Login / Sign Up")

#             auth_mode = st.radio("Choose mode", ["Login", "Sign Up"])

#             email = st.text_input("Email")
#             password = st.text_input("Password", type="password")

#             if st.button("Submit"):
#                 if auth_mode == "Sign Up":
#                     res = sign_up(email, password)
#                 else:
#                     res = sign_in(email, password)

#                 if res.user:
#                     st.session_state.user = res.user
#                     st.success("Logged in successfully")
#                     st.rerun()
#                 else:
#                     st.error("Authentication failed")

#             return
#     if st.button("Logout"):
#         sign_out()
#         st.session_state.user = None
#         st.rerun()
#     st.set_page_config(page_title="Chat with Multiple PDFS", page_icon=":soccer:", layout="wide")
#     #main header of the page
#     st.header("Chat with Multiple PDFS :soccer:")  

#     if "conversation" not in st.session_state:
#         st.session_state.conversation = None

#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []
    
#     conversation  = None
#     pdf_docs = None
#     with st.sidebar:
#         if st.session_state.user and st.session_state.user.id:
#             existing_pdf = has_documents_for_user(st.session_state.user.id)  #check if current already has vectors embedded
#         else:
#             existing_pdf = False
#         if existing_pdf:
#             st.subheader("Existing PDF Documents")
#             st.write("You have already uploaded PDF documents. You can start asking questions about them.")
#             conversation = get_conversation_chain()
#         else:
#             st.subheader("Your PDF Documents")
#             pdf_docs = st.file_uploader("Upload your PDF files here: ", accept_multiple_files=True)
#             if st.button("Upload"):
#                 if not pdf_docs:
#                     st.warning("Please upload at least one PDF.")
#                     return
                
#                 with st.spinner("Processing"):
#                     #get pdf text 
#                     raw_text = get_pdf_text(pdf_docs)

#                     #get the text chunks
#                     text_chunks = get_text_chunks(raw_text)
                    
#                     #create vector store
#                     vectorstore = get_vectorstore(text_chunks, st.session_state.user)

#                     #create conversation chain
#                     st.session_state.conversation = get_conversation_chain()
#                     conversation = st.session_state.conversation

#     #CHAT INPUT
#     # Only show the input box if the user has uploaded PDFs or has documents in the DB
#     if pdf_docs or has_documents_for_user(st.session_state.user.id):
#         user_question = st.chat_input("Ask a question about your documents")
#     else:
#         st.info("You cannot ask questions until you upload PDFs.")
#         user_question = None
   
#     if user_question and conversation:
#         response = conversation.invoke(
#             {"input": user_question},
#             config={"configurable": {"session_id": "streamlit_user"}}
#         )

#         st.session_state.chat_history.append(("user", user_question))
#         st.session_state.chat_history.append(("assistant", response))
    
#     #Display chat hsitory
#     for role, message in st.session_state.chat_history:
#         with st.chat_message(role):
#             st.write(message)

# if __name__ == "__main__": 
#     main()