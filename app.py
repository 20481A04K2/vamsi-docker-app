from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# --- Serve index.html from the same folder ---
@app.route('/')
def home():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

# --- Protected API Endpoint ---
@app.route('/api/protected', methods=['GET'])
def protected_resource():
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization header missing or invalid"}), 401

    token = auth_header.split(' ')[1]

    # Simulated token validation
    if token == "VALID_ID_TOKEN_FROM_OIDC":
        return jsonify({
            "message": "Access granted via OIDC!",
            "data": {
                "user_id": "oidc.hello-user-123",
                "role": "authenticated_user",
                "token_received": token[:30] + "..."
            }
        }), 200
    else:
        return jsonify({
            "message": "Access denied. Token validation failed.",
            "token_status": "Invalid or expired token"
        }), 403


if __name__ == '__main__':
    # Run on all interfaces for Docker/GKE
    app.run(host='0.0.0.0', port=5000)
