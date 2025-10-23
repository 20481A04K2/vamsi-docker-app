from flask import Flask, jsonify, request, render_template
import firebase_admin
from firebase_admin import credentials, auth
import os

# Configure Flask to look for templates (like index.html) in the current directory
app = Flask(__name__, template_folder='.') 

# --- 1. INITIALIZE FIREBASE ADMIN SDK ---
# NOTE: In a real environment, you must initialize the Admin SDK with
# a service account file for token validation to work.
# Without a valid credential, the token verification will fail.
try:
    # We use the default app initialization here, which might work if environment
    # variables are set, but for local testing, the token verification will 
    # likely fail without explicit credentials.
    firebase_admin.initialize_app()
    print("Firebase Admin SDK initialized successfully (using default credentials).")
    ADMIN_SDK_READY = True
except Exception as e:
    # This warning is expected if you are running this in an environment without 
    # Google application default credentials set up.
    print(f"WARNING: Firebase Admin SDK initialization failed: {e}")
    print("Token validation will fail because the Admin SDK could not be configured.")
    ADMIN_SDK_READY = False


# --- Routes to Serve the Frontend ---

@app.route('/')
def home():
    """Serves the main frontend application."""
    # Renders the index.html file, which contains all the frontend logic.
    return render_template('index.html')

@app.route('/api/index')
def api_index():
    """Route requested by the user to serve the token generation page."""
    # Renders the index.html file, providing the same content as the root route.
    return render_template('index.html')

# --- Simplified Gateway/API Endpoints ---

@app.route('/api/test', methods=['GET'])
def test_connection():
    """Unprotected endpoint to confirm Flask server is running and accessible."""
    return jsonify({
        "status": "success",
        "message": "Flask server is online and responding to /api/test!"
    }), 200

@app.route('/api/protected', methods=['GET'])
def protected_resource():
    """
    A protected endpoint that validates the Firebase ID Token using the Admin SDK.
    """
    # 1. Get the Authorization header
    auth_header = request.headers.get('Authorization')
    
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"message": "Authorization header missing or invalid"}), 401
    
    # 2. Extract the token (Firebase ID Token)
    token = auth_header.split(' ')[1]

    if not ADMIN_SDK_READY:
        return jsonify({
            "message": "Access denied.",
            "token_status": "Admin SDK is not initialized, cannot verify token.",
            "guide": "You must configure Firebase Admin SDK credentials (e.g., service account key) for validation to work."
        }), 500

    # 3. VERIFY THE TOKEN using the Admin SDK
    try:
        # This is the core validation step. It verifies the signature, expiry, etc.
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        
        # If verification succeeds, access is granted.
        return jsonify({
            "message": "Access granted! Token verified successfully by Firebase Admin SDK.",
            "data": {
                "user_id": uid,
                "role": "authenticated_firebase_user",
                "token_preview": token[:30] + "...",
                "email_or_phone": decoded_token.get('email', 'N/A')
            }
        }), 200

    except auth.InvalidIdTokenError as e:
        # Handle cases where the token is expired, tampered with, or invalid.
        return jsonify({
            "message": "Access denied. Token validation failed.",
            "token_status": f"Invalid ID Token: {e}",
            "guide": "Your token is invalid, expired, or the Admin SDK credentials are wrong."
        }), 403
    except Exception as e:
        # Catch other errors, like network issues or internal Admin SDK errors.
        return jsonify({
            "message": "Internal Server Error during token verification.",
            "error": str(e)
        }), 500


if __name__ == '__main__':
    # Running on all interfaces (0.0.0.0) for Docker compatibility
    app.run(host='0.0.0.0', port=5000)

