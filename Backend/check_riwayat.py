import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

try:
    supabase: Client = create_client(url, key)
    res = (
        supabase.table("riwayat_diagnosa")
        .select("id, user_id, hasil_diagnosa, gejala_terpilih, tanggal, profiles(name)")
        .order("tanggal", desc=True)
        .limit(5)
        .execute()
    )
    print("Jumlah Baris:", len(res.data) if res.data else 0)
    print("Data:", json.dumps(res.data, indent=2))
except Exception as e:
    print("Error:", str(e))
