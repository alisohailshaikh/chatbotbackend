import os
from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client
import uuid


def get_pdf_text(pdf_doc):
    print("Extracting text from PDF documents...")
    text = ""
    file_name = pdf_doc.name
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    if (len(text) > 0):
        print("Text extracted successfully")
    return text, file_name 

def get_text_chunks(raw_text):
    text_spiltter = CharacterTextSplitter(
        separator="\n", #split by new line
        chunk_size=1000, #len of each chunk
        chunk_overlap=200, #start next chunk 200 characters before the end of the previous chunk to complete all sentences
        length_function=len
    )

    chunks = text_spiltter.split_text(raw_text)
    if (chunks):
        print("Text chunks created successfully")
    return chunks


def get_vectorstore(text_chunks, user_id, file_name):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    USER_ID = user_id

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    document_id = str(uuid.uuid4())
    vectors = embeddings.embed_documents(text_chunks)
    data = []
    for i in range(len(vectors)):
        data.append({
            "content": text_chunks[i],
            "embedding": vectors[i],
            "user_id": USER_ID,
            "metadata": {},
            "document_id": document_id,
            "file_name": file_name
        })
    
    supabase.table("documents").insert(data).execute()

    if (supabase):
        print("Vectorstore created successfully")
    return document_id
