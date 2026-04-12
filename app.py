import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from pdf_utils import get_pdf_text, get_text_chunks, get_vectorstore
from conversation_chain import get_conversation_chain
from check_for_documents import has_documents_for_user
from auth import sign_up, sign_in, sign_out, get_session


def show_auth():
    st.title("Login / Sign Up")

    auth_mode = st.radio("Choose mode", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        res = sign_up(email, password) if auth_mode == "Sign Up" else sign_in(email, password)

        # HANDLE ERRORS FIRST
        if isinstance(res, dict) and "error" in res:
            st.error("Invalid email or password")
            return

        # SUCCESS CASE
        if res and res.user:
            st.session_state.user = res.user
            st.session_state.session = res.session
            st.success("Logged in successfully")
            st.rerun()
        else:
            st.error("Authentication failed")


def main():
    st.set_page_config(page_title="Chat with PDFs", layout="wide")

    # -------------------------
    # SESSION INIT
    # -------------------------
    if "user" not in st.session_state:
        st.session_state.user = None
        st.session_state.session = None

    if st.session_state.session is None:
        session = get_session()
        if session and session.user:
            st.session_state.session = session
            st.session_state.user = session.user

    if "conversations" not in st.session_state:
        st.session_state.conversations = {}

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    if "selected_document_id" not in st.session_state:
        st.session_state.selected_document_id = None

    user = st.session_state.user

    # -------------------------
    # AUTH GATE
    # -------------------------
    if not user:
        show_auth()
        return

    USER_ID = user.id

    # -------------------------
    # LOGOUT
    # -------------------------
    if st.button("Logout"):
        sign_out()
        st.session_state.user = None
        st.session_state.session = None
        st.session_state.conversations = {}
        st.session_state.chat_history = {}
        st.session_state.selected_document_id = None
        st.rerun()

    st.header("Chat with your PDFs 📄")

    # -------------------------
    # CHECK IF USER HAS DOCS
    # -------------------------
    docs = has_documents_for_user(USER_ID)

    # -------------------------
    # SIDEBAR LOGIC
    # -------------------------
    with st.sidebar:
        if docs:
            st.success("Your PDFs")

            selected = st.selectbox(
                "Select a PDF",
                options=docs,
                format_func=lambda x: x["file_name"]
            )

            st.session_state.selected_document_id = selected["document_id"]
            document_id = selected["document_id"]

            if document_id not in st.session_state.conversations:
                st.session_state.conversations[document_id] = get_conversation_chain(
                    st.session_state.user.id,
                    document_id
                )

        else:
            st.subheader("Upload your PDF")
            pdf_doc = st.file_uploader("Upload PDF", accept_multiple_files=False)

            if st.button("Upload"):
                if not pdf_doc:
                    st.warning("Please upload a PDF.")
                    return

                with st.spinner("Processing..."):
                    raw_text, file_name = get_pdf_text(pdf_doc)
                    text_chunks = get_text_chunks(raw_text)

                    document_id = get_vectorstore(text_chunks, USER_ID, file_name)

                    st.session_state.conversations[document_id] = get_conversation_chain(
                        st.session_state.user.id,
                        document_id
                    )

                    st.success("PDF uploaded successfully!")
                    st.rerun()

    # -------------------------
    # CHAT SECTION
    # -------------------------
    if docs:
        user_question = st.chat_input("Ask a question about your documents")

        document_id = st.session_state.selected_document_id

        if user_question and document_id:
            conversation = st.session_state.conversations[document_id]

            response = conversation.invoke(
                {"input": user_question},
                config={"configurable": {"session_id": USER_ID}}
            )

            if document_id not in st.session_state.chat_history:
                st.session_state.chat_history[document_id] = []

            st.session_state.chat_history[document_id].append(("user", user_question))
            st.session_state.chat_history[document_id].append(("assistant", response))

    else:
        st.info("Upload a PDF to start chatting.")

    # -------------------------
    # DISPLAY CHAT
    # -------------------------
    doc_id = st.session_state.selected_document_id

    if doc_id and doc_id in st.session_state.chat_history:
        for role, message in st.session_state.chat_history[doc_id]:
            with st.chat_message(role):
                st.write(message)


if __name__ == "__main__":
    main()