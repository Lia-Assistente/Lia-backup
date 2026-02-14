#!/usr/bin/env python3
"""
Google OAuth Flow for Google Ads API
"""
import json
import http.server
import socketserver
import webbrowser
import urllib.parse
import urllib.request
import threading
import time

# Credentials from Julio
CLIENT_ID = "24548271801-64ek0jftds8g98uuun2ghgkjsuht2ugu.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8080/callback"

# Scopes for Google Ads API
SCOPES = [
    "https://www.googleapis.com/auth/adwords",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive.readonly"
]

def generate_auth_url():
    """Generate the OAuth authorization URL."""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"
    return url

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    """Handle the OAuth callback."""
    auth_code = None
    
    def do_GET(self):
        if self.path.startswith("/callback"):
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            if "code" in params:
                OAuthHandler.auth_code = params["code"][0]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"""
                    <html><body>
                    <h1>Authorization Successful!</h1>
                    <p>You can close this window.</p>
                    <script>setTimeout(() => window.close(), 2000)</script>
                    </body></html>
                """)
            else:
                self.send_response(400)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging

def exchange_code_for_tokens(auth_code):
    """Exchange authorization code for tokens."""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=urllib.parse.urlencode(data).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            tokens = json.loads(response.read().decode())
            return tokens
    except Exception as e:
        print(f"Error exchanging code: {e}")
        return None

def run_oauth_flow():
    """Run the complete OAuth flow."""
    print("Starting Google OAuth Flow...")
    print()
    
    # Generate and display auth URL
    auth_url = generate_auth_url()
    print(f"Authorization URL: {auth_url}")
    print()
    
    # Start local server to receive callback
    PORT = 8080
    with socketserver.TCPServer(("", PORT), OAuthHandler) as httpd:
        print(f"Listening on http://localhost:{PORT}/callback")
        print()
        
        # Open browser for authorization
        print("Opening browser for authorization...")
        webbrowser.open(auth_url)
        
        # Wait for authorization (with timeout)
        print("Waiting for authorization...")
        timeout = 300  # 5 minutes
        start = time.time()
        
        while OAuthHandler.auth_code is None:
            if time.time() - start > timeout:
                print("Timeout waiting for authorization.")
                return None
            time.sleep(1)
        
        print("Authorization code received!")
        print()
        
        # Exchange code for tokens
        print("Exchanging code for tokens...")
        tokens = exchange_code_for_tokens(OAuthHandler.auth_code)
        
        if tokens:
            print()
            print("=== TOKENS ===")
            print(json.dumps(tokens, indent=2))
            
            # Save tokens to file
            with open("/home/julio/.openclaw/workspace/google_oauth_tokens.json", "w") as f:
                json.dump(tokens, f, indent=2)
            print()
            print("Tokens saved to: /home/julio/.openclaw/workspace/google_oauth_tokens.json")
            
            return tokens
        else:
            print("Failed to get tokens.")
            return None

if __name__ == "__main__":
    run_oauth_flow()
