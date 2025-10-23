from flask import Flask, jsonify, request


app = Flask(__name__)


# --- Simplified Gateway/API Endpoints ---


@app.route('/')
def home():
    """Simple health check endpoint."""
    return "OIDC Test Application is Running!", 200


@app.route('/api/protected', methods=['GET'])
def protected_resource():
    """
    A protected endpoint. In a real scenario, you would validate the
    Firebase ID Token sent in the 'Authorization: Bearer <token>' header here.
    """
    # 1. Get the Authorization header
    auth_header = request.headers.get('Authorization')
   
    if not auth_header or not auth_header.startswith('Bearer '):
        # Fail if token is missing
        return jsonify({"message": "Authorization header missing or invalid"}), 401
   
    # 2. Extract the token (e.g., Firebase ID Token)
    # In a real app, you would verify this token using the Firebase Admin SDK.
    token = auth_header.split(' ')[1]
   
    # --- SIMULATED TOKEN VALIDATION ---
    # NOTE: This simple string comparison is intended to FAIL when tested with
    # a real Firebase token (as the frontend sends one), demonstrating the 403 response.
    if token == "VALID_ID_TOKEN_FROM_OIDC":
        # If the token were valid, we'd return real data
        return jsonify({
            "message": "Access granted via OIDC!",
            "data": {
                "user_id": "oidc.hello-user-123",
                "role": "authenticated_user",
                "token_received": token[:30] + "..."
            }
        }), 200
    else:
        # If the token is invalid or missing (in our simple case)
        return jsonify({
            "message": "Access denied. Token validation failed.",
            "token_status": "Invalid or expired token"
        }), 403


if __name__ == '__main__':
    # Running on all interfaces (0.0.0.0) for Docker compatibility
    app.run(host='0.0.0.0', port=5000)
