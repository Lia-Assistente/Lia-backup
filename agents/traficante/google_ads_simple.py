#!/usr/bin/env python3
"""
Google Ads API Simple Client
Usa requests direto para a Google Ads API v14
"""
import json
import os
import requests
from datetime import datetime, timedelta

# Carregar tokens
TOKENS_FILE = "/home/julio/.openclaw/workspace/google_oauth_tokens.json"

def load_tokens():
    with open(TOKENS_FILE) as f:
        return json.load(f)

def refresh_token_if_needed(tokens):
    """Renova token se necessário."""
    # Por simplicidade, vamos usar o access_token atual
    # Em produção, verificaria expires_in
    return tokens

def get_customer_ids(tokens):
    """Lista customer IDs da conta."""
    # API de gerenciamento de contas
    url = "https://mybusinessaccountmanagement.googleapis.com/v1/accounts"
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        # Retorna lista de customer IDs
        return data.get("accountBindings", [])
    else:
        print(f"Erro: {response.status_code}")
        print(response.text)
        return []

def get_gaql_query(tokens, customer_id, query):
    """Executa query GAQL."""
    url = f"https://googleads.googleapis.com/v14/{customer_id}:searchStream"
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json",
        "developer-token": os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    }
    
    body = {"query": query}
    
    response = requests.post(url, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro na query: {response.status_code}")
        print(response.text)
        return None

def simple_daily_check():
    """Verificação simples."""
    print("=" * 60)
    print("GOOGLE ADS - CHECKLIST DIÁRIO")
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print()
    
    tokens = load_tokens()
    tokens = refresh_token_if_needed(tokens)
    
    # Tentar obter customer ID
    print("🔍 Verificando contas...")
    
    # Customer ID pode ser obtido de várias formas
    # O Julio pode ter múltiplas contas vinculadas
    # Por enquanto, vamos listar o que conseguimos
    
    print()
    print("⚠️ Para completar a integração, preciso:")
    print()
    print("1. Developer Token do Google Ads (no Google Ads UI)")
    print("   - Ferramentas → API Center → Developer Token")
    print()
    print("2. Customer ID da conta principal")
    print("   - Formato: 123-456-7890")
    print()
    print("3. Verificar se API está habilitada no Google Cloud Console")
    print()
    
    print("📋 Status atual:")
    print(f"   - Access Token: {tokens['access_token'][:30]}...")
    print(f"   - Scopes: {tokens['scope'][:80]}...")
    print(f"   - Token Type: {tokens['token_type']}")

if __name__ == "__main__":
    simple_daily_check()
