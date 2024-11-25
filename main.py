from flask import Flask, request, jsonify
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os
import json

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'  # Ensure transport errors are strict
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'  # Optional: allow token scope relaxation

app = Flask(__name__)

# File paths and scopes
CLIENT_SECRET_FILE = 'client_secret.json'  # Path to your client_secret.json file
TOKEN_FILE = 'token.json'
SCOPES = ['https://www.googleapis.com/auth/documents']

@app.route('/privacy', methods=['GET'])
def privacy():
    """
    Returns the privacy policy text as an HTML page.
    """
    privacy_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Policy</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                line-height: 1.6;
            }
            h1 {
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>Privacy Policy</h1>
        <p>
            This application uses Google APIs to perform its operations. The app accesses user data
            only as necessary to fulfill its functionality, such as creating Google Docs. No user data
            is shared or stored beyond what is required to execute the requested functionality.
        </p>
        <p>
            The app complies with Google's User Data Policy, including the Limited Use requirements.
        </p>
        <p>
            If you have any questions or concerns about your data privacy, please contact us.
        </p>
    </body>
    </html>
    """
    return privacy_html

@app.route('/startAuth', methods=['GET'])
def start_auth():
    """
    Initiates the OAuth flow to authenticate the user.
    Returns the authorization URL for the user to visit and authenticate.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = 'https://31bc-2407-d000-1a-f25e-a8fc-c648-d43e-cd47.ngrok-free.app/handleAuth'
    auth_url, _ = flow.authorization_url(prompt='consent')
    return jsonify({'auth_url': auth_url}), 200


@app.route('/handleAuth', methods=['GET'])
def handle_auth():
    """
    Handles the OAuth redirect, exchanges the authorization code for tokens,
    and saves them to a file for future use.
    """
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = 'https://31bc-2407-d000-1a-f25e-a8fc-c648-d43e-cd47.ngrok-free.app/handleAuth'

    # Process the redirect URL to fetch tokens
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)

    # Save credentials to a file
    creds = flow.credentials
    with open(TOKEN_FILE, 'w') as token_file:
        token_file.write(creds.to_json())

    return jsonify({'message': 'Authentication successful! You can now create Google Docs.'}), 200


@app.route('/createDoc', methods=['POST'])
def create_doc():
    """
    Creates a new Google Doc with the given title and content.
    Requires prior authentication via OAuth.
    """
    data = request.json
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': 'Title and content are required'}), 400

    try:
        # Load credentials
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as token_file:
                creds_json = json.load(token_file)
                creds = Credentials.from_authorized_user_info(creds_json)
        else:
            return jsonify({'error': 'User not authenticated. Please authenticate at /startAuth'}), 401

        # Initialize the Google Docs API
        service = build('docs', 'v1', credentials=creds)

        # Create a new document
        doc = service.documents().create(body={"title": title}).execute()
        doc_id = doc.get('documentId')

        # Add content to the document
        requests = [
            {
                'insertText': {
                    'location': {
                        'index': 1,
                    },
                    'text': content,
                }
            }
        ]
        service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()

        # Return the document URL
        doc_url = f"https://docs.google.com/document/d/{doc_id}"
        return jsonify({'message': f'Document created successfully: {doc_url}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
