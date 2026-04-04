from supabase import create_client
import os

def has_documents_for_user() -> bool:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY") 
    user_id = os.getenv("TESTDB_USER_ID")
    supabase = create_client(url, key)
    
    result = (
        supabase
        .table("documents")
        .select("id")
        .eq("user_id", user_id)  # Filter by user
        .limit(1)                # Only need one document
        .execute()
    )

    if result.data and len(result.data) > 0:
        return True
    return False