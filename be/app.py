from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
import os

# Inisialisasi aplikasi
app = Flask(__name__)
CORS(app)

# Environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Initialize Supabase client
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("✅ Supabase client initialized")
else:
    print("❌ Supabase environment variables missing")
    supabase = None

@app.route("/")
def home():
    return jsonify({
        "message": "Flask Render deployment works!",
        "status": "success"
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

        # Validasi email sederhana
        if "@" not in email:
            return jsonify({"error": "Invalid email format"}), 400

        result = supabase.table("users").insert({
            "email": email, 
            "password": password
        }).execute()

        if hasattr(result, 'error') and result.error:
            return jsonify({"error": str(result.error)}), 400

        return jsonify({
            "message": "User registered successfully",
            "data": result.data
        }), 201
        
    except Exception as e:
        print(f"Error in /register: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    # Untuk development saja
    # Di production, gunicorn akan menangani
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)