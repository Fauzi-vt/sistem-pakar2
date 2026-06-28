import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL or "", SUPABASE_KEY or "")

def check_db():
    try:
        # We can try to use supabase.rpc or raw SQL if we have pg credentials.
        # But wait, supabase client doesn't support raw SQL queries like querying information_schema directly unless exposed via RPC or using psycopg2 with connection string.
        # Let's check what tables we have using standard supabase rest API if possible, or just note it.
        pass
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_db()
