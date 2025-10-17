from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

app = Flask(__name__)
CORS(app)

# Gunakan environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

print("=== Checking Environment Variables ===")
print(f"PORT: {os.environ.get('PORT')}")
print(f"SUPABASE_URL exists: {SUPABASE_URL is not None}")
print(f"SUPABASE_KEY exists: {SUPABASE_KEY is not None}")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Supabase client initialized successfully")
else:
    print("ERROR: Missing Supabase environment variables")
    supabase = None

@app.route("/")
def home():
    return jsonify({
        "message": "Flask Render deployment works!",
        "status": "success",
        "supabase_configured": SUPABASE_URL is not None and SUPABASE_KEY is not None
    })

@app.route("/health")
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route("/register", methods=["POST"])
def register():
    try:
        if not supabase:
            return jsonify({"error": "Database not configured"}), 500
            
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        result = supabase.table("users").insert({
            "email": email, 
            "password": password
        }).execute()

        return jsonify({
            "message": "User registered successfully",
            "data": result.data
        }), 201
        
    except Exception as e:
        print(f"Error in /register: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# Hapus block ini untuk production, atau pastikan debug=False
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)  # debug=False untuk production