from langchain_openai import OpenAIEmbeddings
from supabase import create_client
import os

def retrieve_documents(query, user_id, document_id):

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    supabase = create_client(url, key)

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    query_embedding = embeddings.embed_query(query)

    response = supabase.rpc(
        "match_documents",
        {
            "query_embedding": query_embedding,
            "match_count": 5,
            "filter_user_id": user_id,
            "filter_document_id": document_id
        }
    ).execute()

    return [doc["content"] for doc in response.data]