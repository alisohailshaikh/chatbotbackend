import os

from pypdf import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import SupabaseVectorStore
from supabase import create_client
from dotenv import load_dotenv



def get_pdf_text(pdf_docs):
    print("Extracting text from PDF documents...")
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    if (len(text) > 0):
        print("Text extracted successfully")
    return text 

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


def get_vectorstore(text_chunks):
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase = create_client(url, key)
    USER_ID = os.getenv("TESTDB_USER_ID")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectors = embeddings.embed_documents(text_chunks)
    data = []
    for i in range(len(vectors)):
        data.append({
            "content": text_chunks[i],
            "embedding": vectors[i],
            "user_id": USER_ID,
            "metadata": {}
        })
    
    supabase.table("documents").insert(data).execute()

    if (supabase):
        print("Vectorstore created successfully")
    return supabase
