# Google Docs Creator API with CustomGPT Integration

This project provides an API to create Google Docs using Google OAuth authentication. It is designed for integration with **CustomGPT** or similar platforms to enable seamless document creation workflows.

## **Features**
- **Authentication**: Allows users to authenticate with their Google account via OAuth 2.0.
- **Google Docs Creation**: Enables users to create Google Docs with a title and content.
- **Privacy Policy**: Provides a publicly accessible privacy policy endpoint for transparency.

---

## **Endpoints**
1. **`GET /startAuth`**
   - Initiates the Google OAuth flow by returning an authentication URL.
   - **Response**: JSON with the `auth_url` key.

2. **`GET /handleAuth`**
   - Handles the Google OAuth callback, exchanges the authorization code for tokens, and saves them locally.

3. **`POST /createDoc`**
   - Creates a Google Doc with the specified title and content.
   - **Request Body**:
     ```json
     {
       "title": "Your Document Title",
       "content": "The content of the document."
     }
     ```
   - **Response**: JSON containing the URL of the created document.

4. **`GET /privacy`**
   - Displays the privacy policy as an HTML page in the browser.

---

## **Setup Instructions**

### **Prerequisites**
1. Install Python (3.7 or above).
2. Install the required libraries:
   ```bash
   pip install flask google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```
3. Download your Google OAuth credentials (`client_secret.json`) from the [Google Cloud Console](https://console.cloud.google.com/).

### **Google Cloud Configuration**
1. Go to **APIs & Services > Credentials**.
2. Enable the **Google Docs API**.
3. Create an **OAuth 2.0 Client ID**:
   - Application type: **Web Application**.
   - Add the following as **Authorized Redirect URIs**:
     - For local development: `http://127.0.0.1:5000/handleAuth`
     - For production (via ngrok or server): `https://YOUR_NGROK_URL/handleAuth`
4. Download the `client_secret.json` file and place it in the root directory of this project.

---

### **How to Run**
1. Clone this repository:
   ```bash
   git clone https://github.com/your-repo/google-docs-creator.git
   cd google-docs-creator
   ```

2. Place the `client_secret.json` file in the root directory.

3. Run the Flask application:
   ```bash
   python app.py
   ```

4. Expose your app to the internet using ngrok:
   ```bash
   ngrok http 5000
   ```
   Note the HTTPS URL (e.g., `https://YOUR_NGROK_URL`) provided by ngrok.

---

### **Usage**

1. **Authenticate with Google**:
   - Access the `/startAuth` endpoint:
     ```bash
     GET https://YOUR_NGROK_URL/startAuth
     ```
   - Open the returned `auth_url` in a browser to log in and grant permissions.
   - Google redirects to `/handleAuth`, where credentials are saved.

2. **Create a Google Doc**:
   - Call the `/createDoc` endpoint:
     ```bash
     POST https://YOUR_NGROK_URL/createDoc
     Content-Type: application/json
     Body:
     {
       "title": "My Document",
       "content": "This is the content of my document."
     }
     ```

3. **View Privacy Policy**:
   - Visit the `/privacy` endpoint:
     ```bash
     GET https://YOUR_NGROK_URL/privacy
     ```

---

## **Project Structure**

```plaintext
google-docs-creator/
├── app.py                # Main Flask application
├── client_secret.json    # Google OAuth credentials (not included, must be added)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## **Important Notes**
- **Authentication Tokens**: OAuth tokens are stored locally in `token.json`. Keep this file secure.
- **Redirect URIs**: Ensure that your redirect URIs in the Google Cloud Console match the ones used in your app (local and ngrok URLs).
- **Privacy Policy**: Update the `/privacy` endpoint text if necessary to reflect your actual data usage practices.

---

## **Contributing**
Contributions are welcome! Feel free to submit a pull request or open an issue to improve the project.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
