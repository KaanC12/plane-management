from flask import Flask, request, abort, jsonify, session, send_from_directory
import requests
import os
import jwt
import psycopg2
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from vision import Render


app = Flask(__name__) 
JAVA_API = "http://localhost:8080"
UPLOAD_FOLDER = os.path.abspath("../uploads")
SECRET = "F868C47C-663C-4D71-AFB9-3FB52EFEE393"
API_SECRET = "bdbf0c816b1f27d8ab45d91f2f07de541379b75ee3f83be41c21c61e1930ea09"

# ======================== Verification =====================
# Token verification
def require_token():
    auth = request.headers.get("Authorization")
    if not auth:
        abort(401, "Missing token")
    
    try:
        token = auth.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        abort(401, "Token expired")
    except jwt.InvalidTokenError:
        abort(401, "Invalid token")

# 3rd party dev auth.
def api_auth(company_name : str, api_hash_key : str) -> bool:
    conn = psycopg2.connect(
        host="localhost",
        database="airmanagement",
        user="kaan",
    )

    cun = conn.cursor()

    cun.execute(
        """
        SELECT * FROM devs
        WHERE company_name = %s
        AND api_key_hash = %s
        """,
        (company_name, api_hash_key)
    )

    dev = cun.fetchone()
    
    if not dev:
        return False
    else:
        return True
    
# Generate token
def generate_token():
    return jwt.encode({}, API_SECRET, algorithm="HS256")

# Verify token
def verify_token(token) -> bool:
    try:
        jwt.decode(token, API_SECRET, algorithms="HS256")
        return True
    except:
        return False

# ================== Login Page =================
# Login request
@app.route("/auth/login", methods=['POST'])
def login():
    data = request.get_json()
    r = requests.post(
        f"{JAVA_API}/auth/login",
        json=data,
        timeout=5
    )
    if r.status_code != 200:
        return jsonify(r.json(), r.status_code)
    
    return jsonify(r.json()), 200

# Register request
@app.route("/auth/register", methods=['POST'])
def register():
    data = request.get_json()
    r = requests.post(
        f"{JAVA_API}/auth/register",
        json=data,
        timeout=5
    )
    if r.status_code != 200:
        return jsonify(r.status_code)

    return jsonify({"message": "User registered"}), r.status_code

# ===================== Plane =============================

# Gives paths of the planes. 
@app.route("/plane/<email>/get_planes", methods=['GET'])
def get_planes(email):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing token"}), 401
    r = requests.get(
        f"{JAVA_API}/plane/{email}/get_planes",
        headers={
            "Authorization": f"Bearer {auth_header}"
        }
    )

    if r.status_code != 200:
        return jsonify({"error": "Spring error"}), r.status_code

    return jsonify(r.json()), 200

# Forward the plane image.
@app.route("/uploads/planes/<filename>")
def serve_plane_iamge(filename):
    payload = require_token()
    return send_from_directory(
        os.path.join(UPLOAD_FOLDER, "planes"),
        filename
    )

# Save plane.
@app.route("/plane/save", methods=["POST"])
def save_plane():
    token = request.headers.get("Authorization")
    data = request.get_json()
    email = data['email']
    aircraftName = data['aircraftName']
    data = {
        "email": email,
        "aircraftName": aircraftName
    }
    r = requests.post(
        f"{JAVA_API}/plane/save",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    if r.status_code != 200:
        abort(400)

    return jsonify(r.json()), 200


# ================== OCR =======================
@app.route("/forms/extract", methods=["POST"])
def extract():
    key = require_token()
    if "file" not in request.files:
        return jsonify({'error': 'File is missing'})

    file = request.files["file"]

    file_bytes = file.read()
    
    render = Render(img_bytes=file_bytes, key_words=["1.", "2.", "3.", "4.", "5."])
    render.classify_document()
    document_type = render.type

    if document_type == "box_form":
        render.text_from_box()
        data = render.result
    else:
        render.text_from_letter()
        data = render.result
    
    return jsonify({"data": data}), 200


# ================= Charging Station =====================
@app.route("/get-stations", methods=["GET"])
def get_stations():
    token = request.headers.get("Authorization")
    r = requests.get(
        f"{JAVA_API}/charging-point/get-stations",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    return jsonify(r.json()), r.status_code


#======================= 3rd party dev =====================
@app.route("/api-login", methods=["POST"])
def dev_auth():
    data = request.get_json()
    company_name = data["company-name"]
    api_hash_key = data["api-key"]

    if not api_auth(company_name, api_hash_key):
        abort(401)
    
    token = generate_token()
    
    return jsonify({"token": f"{token}"}), 200

@app.route("/verify-api", methods=["POST"])

def verify_api():
    data = request.get_json()
    token = data["token"]

    if not verify_token(token):
        abort(401)
    
    return jsonify({"message": "done"}), 200

@app.route("/add-station", methods=["POST"])
def add_station():
    
    data = request.get_json()

    name = data["name"]
    kw = data["kw"]
    available = data["isAvailable"]
    lat = data["latitude"]
    lng = data["longitude"]

    if not name or not kw or not available or not lat or not lng:
        abort(401)

    conn = psycopg2.connect(
        host="localhost",
        database="airmanagement",
        user="kaan"
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO charging_station
    (name, kw, is_available, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(query, (name, kw, available, lat, lng))

    conn.commit()

    return jsonify({"message": "station added"}), 200
    
    

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)