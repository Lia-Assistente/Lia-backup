#!/usr/bin/env python3
"""
Google Ads API - Versão Simples com tratamento de erros
"""
import json
import requests

TOKENS_FILE = "/home/julio/.openclaw/workspace/google_oauth_tokens.json"
DEVELOPER_TOKEN = "-XLn0UmUhWfiGDWcJYu0qg"  # Do Julio
CUSTOMER_ID = "830-923-9621"

def load_tokens():
    with open(TOKENS_FILE) as f:
        return json.load(f)

def simple_ads_check():
    tokens = load_tokens()
    
    print("=" * 60)
    print("📊 GOOGLE ADS - VERIFICAÇÃO RÁPIDA")
    print("=" * 60)
    print()
    
    print("Configuração atual:")
    print(f"  Customer ID: {CUSTOMER_ID}")
    print(f"  Developer Token: {DEVELOPER_TOKEN[:15]}...")
    print(f"  Access Token: {tokens['access_token'][:30]}...")
    print()
    
    # Tentar API de accounts
    url = f"https://googleads.googleapis.com/v14/customers/{CUSTOMER_ID}/googleAds:searchStream"
    
    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "developer-token": DEVELOPER_TOKEN,
        "Content-Type": "application/json"
    }
    
    query = """
        SELECT campaign.id, campaign.name, campaign.status
        FROM campaign
        LIMIT 5
    """
    
    print(f" Fazendo запрос para: {url}")
    print()
    
    try:
        response = requests.post(url, headers=headers, json={"query": query}, timeout=30)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500] if response.text else 'Vazio'}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Sucesso! {len(data)} resultados")
            print(json.dumps(data, indent=2)[:1000])
        elif response.status_code == 401:
            print("\n🔐 Erro 401 - Token inválido ou expirado")
            print("Possíveis causas:")
            print("  - Token expirou")
            print("  - scopes não permitem acesso a esta conta")
        elif response.status_code == 403:
            print("\n🚫 Erro 403 - Sem permissão")
            print("Possíveis causas:")
            print("  - Developer Token em modo teste")
            print("  - API não habilitada no Google Cloud")
            print("  - Customer ID não vinculado")
        else:
            print(f"\n❌ Erro {response.status_code}")
            
    except Exception as e:
        print(f"\nExceção: {e}")

if __name__ == "__main__":
    simple_ads_check()
