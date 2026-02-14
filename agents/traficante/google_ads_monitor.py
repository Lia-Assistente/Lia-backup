#!/usr/bin/env python3
"""
Google Ads Daily Monitor - Para o agente Traficante
Usa google-ads library oficial
"""
import os
import sys
from datetime import datetime, timedelta
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Developer Token (do Julio)
DEVELOPER_TOKEN = "-XLn0UmUhWfiGDWcJYu0qg"
CUSTOMER_ID = "830-923-9621"

def load_tokens():
    """Carrega tokens OAuth do arquivo."""
    import json
    with open("/home/julio/.openclaw/workspace/google_oauth_tokens.json") as f:
        return json.load(f)

def get_client():
    """Inicializa cliente Google Ads."""
    tokens = load_tokens()
    
    config = {
        "developer_token": DEVELOPER_TOKEN,
        "refresh_token": tokens["refresh_token"],
        "client_id": "24548271801-64ek0jftds8g98uuun2ghgkjsuht2ugu.apps.googleusercontent.com",
        "client_secret": "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",
        "use_proto_plus": True,
    }
    
    return GoogleAdsClient.load_from_dict(config)

def get_campaigns(client, customer_id, days=7):
    """Obtém métricas de campanhas."""
    ga_service = client.get_service("GoogleAdsService")
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            campaign.status,
            campaign.advertising_channel_type,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            metrics.ctr,
            metrics.all_conversions,
            metrics.all_conversions_value,
            metrics.average_cpc,
            metrics.average_cpm,
            metrics.clicks_per_query,
            metrics.conversions_per_query
        FROM campaign
        WHERE segments.date DURING LAST_{days}_DAYS
        ORDER BY metrics.cost_micros DESC
    """
    
    try:
        search_request = client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = customer_id
        search_request.query = query
        
        results = []
        for response in ga_service.search_stream(search_request):
            for row in response.results:
                campaign = row.campaign
                metrics = row.metrics
                
                results.append({
                    "id": campaign.id.value,
                    "name": campaign.name.value if campaign.name else "Sem nome",
                    "status": campaign.status.name,
                    "type": campaign.advertising_channel_type.name,
                    "impressions": metrics.impressions.value if metrics.impressions else 0,
                    "clicks": metrics.clicks.value if metrics.clicks else 0,
                    "cost": (metrics.cost_micros.value / 1_000_000) if metrics.cost_micros else 0,
                    "conversions": metrics.conversions.value if metrics.conversions else 0,
                    "conversions_value": metrics.conversions_value.value if metrics.conversions_value else 0,
                    "ctr": (metrics.ctr.value * 100) if metrics.ctr else 0,
                    "avg_cpc": (metrics.average_cpc.value / 1_000_000) if metrics.average_cpc else 0,
                    "roas": (metrics.conversions_value.value / (metrics.cost_micros.value / 1_000_000)) 
                           if metrics.cost_micros and metrics.conversions_value and metrics.cost_micros.value > 0 else 0,
                })
        
        return results
    
    except GoogleAdsException as e:
        print(f"Google Ads API Error: {e}")
        return []

def analyze_campaign(camp):
    """Analisa saúde de uma campanha."""
    issues = []
    warnings = []
    status = "🟢"
    
    # Check CTR
    if camp["clicks"] > 0:
        if camp["ctr"] < 1:
            issues.append(f"CTR muito baixo: {camp['ctr']:.2f}%")
        elif camp["ctr"] < 2:
            warnings.append(f"CTR abaixo da média: {camp['ctr']:.2f}%")
    
    # Check CPC
    if camp["clicks"] > 0 and camp["avg_cpc"] > 10:
        warnings.append(f"CPC alto: R$ {camp['avg_cpc']:.2f}")
    
    # Check ROAS
    if camp["conversions"] > 0 and camp["roas"] < 2:
        warnings.append(f"ROAS baixo: {camp['roas']:.2f}x")
    
    # Check Status
    if camp["status"] == "PAUSED":
        warnings.append("⚠️ Campanha pausada")
    
    # Check Spend vs Conversions
    if camp["cost"] > 100 and camp["conversions"] == 0:
        issues.append("💸 Gastando sem converter!")
    
    if issues:
        status = "🔴"
    elif warnings:
        status = "🟡"
    
    return status, issues, warnings

def print_daily_report():
    """Imprime relatório diário."""
    print("=" * 70)
    print("📊 GOOGLE ADS - RELATÓRIO DIÁRIO")
    print(f"🕐 Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"👤 Customer ID: {CUSTOMER_ID}")
    print("=" * 70)
    print()
    
    client = get_client()
    campaigns = get_campaigns(client, CUSTOMER_ID, days=7)
    
    if not campaigns:
        print("⚠️ Nenhuma campanha encontrada ou erro na API")
        return
    
    # Resumo geral
    total_spend = sum(c["cost"] for c in campaigns)
    total_clicks = sum(c["clicks"] for c in campaigns)
    total_conversions = sum(c["conversions"] for c in campaigns)
    total_value = sum(c["conversions_value"] for c in campaigns)
    
    print("📈 RESUMO GERAL (Últimos 7 dias)")
    print("-" * 50)
    print(f"💰 Investimento Total: R$ {total_spend:,.2f}")
    print(f"👆 Total de Cliques: {total_clicks:,}")
    print(f"🎯 Total de Conversões: {total_conversions:,}")
    print(f"💎 Valor das Conversões: R$ {total_value:,.2f}")
    if total_spend > 0:
        print(f"📊 CPA Médio: R$ {total_spend/total_conversions:.2f}" if total_conversions > 0 else "📊 CPA: N/A")
        print(f"📈 ROAS Médio: {total_value/total_spend:.2f}x" if total_spend > 0 else "📈 ROAS: N/A")
    print()
    
    # Detalhamento por campanha
    print("📋 DETALHAMENTO POR CAMPANHA")
    print("-" * 70)
    print(f"{'Status':<5} {'Campanha':<35} {'Gasto':>10} {'Cliques':>7} {'CTR':>6} {'Conv':>5} {'CPA':>8}")
    print("-" * 70)
    
    issues_count = 0
    for camp in campaigns:
        status, issues, warnings = analyze_campaign(campaign := camp)
        
        print(f"{status:<5} {campaign['name'][:35]:<35} "
              f"R$ {campaign['cost']:>8,.0f} {campaign['clicks']:>7} "
              f"{campaign['ctr']:>5.2f}% {campaign['conversions']:>5} "
              f"R$ {campaign['cost']/campaign['conversions']:>7.2f}" if campaign['conversions'] > 0 else "   N/A")
        
        if issues:
            for issue in issues:
                print(f"   🔴 {issue}")
                issues_count += 1
        elif warnings:
            for warn in warnings:
                print(f"   🟡 {warn}")
    
    print("-" * 70)
    print()
    
    # Alertas
    if issues_count > 0:
        print("⚠️ AÇÕES NECESSÁRIAS:")
        print(f"   - {issues_count} problema(s) crítico(s) encontrado(s)")
        print()
    
    # Próximos passos sugeridos
    print("💡 SUGESTÕES:")
    for camp in campaigns:
        _, issues, warnings = analyze_campaign(camp)
        if issues:
            print(f"   - Revisar: {camp['name'][:40]}")
        elif warnings and camp["cost"] > 100:
            print(f"   - Otimizar: {camp['name'][:40]}")

if __name__ == "__main__":
    print_daily_report()
