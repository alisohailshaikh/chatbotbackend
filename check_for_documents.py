from supabase import create_client
import os

def has_documents_for_user(user_id) -> bool:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") 
    supabase = create_client(url, key)
    
    result = (
        supabase
        .table("documents")
        .select("document_id", "file_name")  # Only select the document_id
        .eq("user_id", user_id)  # Filter by user
        .limit(1)                # Only need one document
        .execute()
    )

    if result.data and len(result.data) > 0:
        return result.data
    return None