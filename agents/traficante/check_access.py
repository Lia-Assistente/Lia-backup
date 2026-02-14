#!/usr/bin/env python3
"""
Verifica acesso às contas Google Ads
"""
import json
import requests
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os

TOKENS_FILE = "/home/julio/.openclaw/workspace/google_oauth_tokens.json"

def load_tokens():
    with open(TOKENS_FILE) as f:
        return json.load(f)

def check_accounts():
    tokens = load_tokens()
    
    creds = Credentials(
        token=tokens["access_token"],
        refresh_token=tokens["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id="24548271801-64ek0jftds8g98uuun2ghgkjsuht2ugu.apps.googleusercontent.com",
        client_secret="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",
        scopes=[
            "https://www.googleapis.com/auth/adwords",
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/calendar.readonly", 
            "https://www.googleapis.com/auth/drive.readonly"
        ]
    )
    
    # Refresh token
    creds.refresh(Request())
    print(f"Token renovado: {creds.token[:30]}...")
    
    # Tentar acessar Google Ads API com o novo token
    # Primeiro, verificar contas via OAuth
    url = "https://ads.google.com/aw/billingAccounts"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Content-Type": "application/json"
    }
    
    # Tentar API de gestão de contas
    print("\nVerificando contas Google Ads...")
    
    # Método alternativo: usar Management API
    url = "https://www.googleapis.com/dfatrafficking/v1.1/accounts"
    r = requests.get(url, headers=headers)
    print(f"\nDFA API: {r.status_code}")
    print(r.text[:500] if r.text else "Vazio")
    
    # Tentar account linking
    print("\nVerificando OAuth consents...")
    
    # Verificar scopes do token atual
    print(f"\nScopes autorizados:")
    for scope in tokens.get("scope", "").split():
        print(f"  - {scope}")

if __name__ == "__main__":
    check_accounts()
