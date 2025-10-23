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
    A protected endpoint. The logic is corrected to allow the real Firebase ID Token 
    to pass the **simulated** check for demonstration purposes.
    """
    # 1. Get the Authorization header
    auth_header = request.headers.get('Authorization')
   
    if not auth_header or not auth_header.startswith('Bearer '):
        # Fail if token is missing
        return jsonify({"message": "Authorization header missing or invalid"}), 401
   
    # 2. Extract the token (e.g., Firebase ID Token)
    token = auth_header.split(' ')[1]
   
    # --- SIMULATED TOKEN VALIDATION (CORRECTED) ---
    # The original check: if token == "VALID_ID_TOKEN_FROM_OIDC" always failed.
    # This corrected check allows any non-empty token to pass.
    if token and len(token.split('.')) == 3: # Check if it looks like a JWT (3 parts) and is not empty
        # If the token exists (and looks like a JWT), we return success.
        return jsonify({
            "message": "Access granted! (Token check bypassed for demonstration)",
            "data": {
                "user_id": "oidc.hello-user-123",
                "role": "authenticated_user",
                "token_received": token[:30] + "..."
            }
        }), 200
    else:
        # This will catch missing/empty tokens or tokens that are not JWT-like
        return jsonify({
            "message": "Access denied. Token validation failed.",
            "token_status": "Token missing or malformed"
        }), 403

if __name__ == '__main__':
    # Running on all interfaces (0.0.0.0) for Docker compatibility
    app.run(host='0.0.0.0', port=5000)
