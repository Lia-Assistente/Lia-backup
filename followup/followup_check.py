#!/usr/bin/env python3
"""
Follow-up Lia - Monitoramento de Tarefas via Notion API
Usa o modelo local Qwen para verificar tarefas a cada 5 minutos
"""
import json
import time
from datetime import datetime
from pathlib import Path

# Configuração
STATE_FILE = "/home/julio/.openclaw/workspace/followup/state.json"
LAST_CHECK_FILE = "/home/julio/.openclaw/workspace/followup/last_check.txt"

def get_state():
    """Carrega estado atual."""
    if Path(STATE_FILE).exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"pending_tasks": [], "last_check": None}

def save_state(state):
    """Salva estado."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def update_last_check():
    """Atualiza timestamp do último check."""
    with open(LAST_CHECK_FILE, "w") as f:
        f.write(datetime.now().isoformat())

def get_last_check():
    """Retorna timestamp do último check."""
    if Path(LAST_CHECK_FILE).exists():
        with open(LAST_CHECK_FILE) as f:
            return f.read().strip()
    return None

def check_notion_tasks():
    """
    Verifica tarefas no Notion.
    Nota: Implementação completa depende da API do Notion.
    Por enquanto, retorna status placeholder.
    """
    state = get_state()
    last_check = get_last_check()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "last_notion_check": last_check,
        "pending_count": len(state.get("pending_tasks", [])),
        "pending_tasks": state.get("pending_tasks", []),
        "new_tasks": [],
        "status": "pending_notion_api"  # Aguardando configuração da API
    }
    
    return result

def print_status():
    """Imprime status atual do monitoramento."""
    result = check_notion_tasks()
    
    print("=" * 60)
    print("📋 FOLLOW-UP LIA - STATUS")
    print(f"🕐 {result['timestamp']}")
    print("=" * 60)
    print()
    
    print(f"Status: {result['status']}")
    print(f"Tarefas pendentes: {result['pending_count']}")
    print(f"Último check Notion: {result['last_notion_check'] or 'Nunca'}")
    print()
    
    if result['pending_tasks']:
        print("Tarefas pendentes:")
        for task in result['pending_tasks']:
            print(f"  - {task}")
        print()
    
    if result['new_tasks']:
        print("🆕 Novas tarefas:")
        for task in result['new_tasks']:
            print(f"  - {task}")
        print()

if __name__ == "__main__":
    print_status()
