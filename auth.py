from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)


def sign_up(email, password):
    try:
        return supabase.auth.sign_up({
            "email": email,
            "password": password
        })
    except Exception as e:
        return {"error": str(e)}


def sign_in(email, password):
    try:
        return supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
    except Exception as e:
        return {"error": str(e)}


def sign_out():
    supabase.auth.sign_out()

def get_session():
    return supabase.auth.get_session()