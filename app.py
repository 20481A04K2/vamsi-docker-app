from flask import Flask
from google.cloud import secretmanager
import os

app = Flask(__name__)

# Function to fetch secrets from Google Cloud Secret Manager
def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/secrets/{secret_name}/versions/latest"
    secret = client.access_secret_version(name=secret_path)
    return secret.payload.data.decode("UTF-8")

@app.route('/')
def home():
    try:
        # Fetch secret values
        secret_data = get_secret("my-app-secret")
        
        # Assuming secret_data is a JSON string like {"db_user": "vamsi", "db_pass": "securepassword123", "api_key": "your-api-key-value"}
        import json
        secret_json = json.loads(secret_data)

        db_user = secret_json.get("db_user", "not-found")
        db_pass = secret_json.get("db_pass", "not-found")
        api_key = secret_json.get("api_key", "not-found")

        return f"Hello from Vamsi's Docker App!<br>DB User: {db_user}<br>DB Password: {db_pass}<br>API Key: {api_key}"

    except Exception as e:
        return f"Failed to retrieve secrets: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
