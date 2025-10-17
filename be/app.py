# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Insert ke tabel Supabase
    result = supabase.table("users").insert({"email": email, "password": password}).execute()

    # Versi baru supabase-py pakai .data untuk ambil hasil
    return jsonify(result.data), 201

if __name__ == "__main__":
    app.run(debug=True)
