# Configuração do Agente Traficante

## Como usar o Traficante

### 1. Via OpenClaw (sub-agent)

```bash
# Iniciar sessão do Traficante
/session_new --name traficante --agent traffic_specialist

# Ou como sub-agent
openclaw sessions_spawn --agent traffic_specialist --task "Analisa as campanhas Google Ads de hoje"
```

### 2. Diretamente

```bash
python3 /home/julio/.openclaw/workspace/agents/traficante/google_ads_monitor.py
```

## Pasta do Agente

```
/home/julio/.openclaw/workspace/agents/traficante/
├── SOUL.md          # Persona do Traficante
├── USER.md          # Contexto do Julio
├── SKILLS.md        # Ferramentas disponíveis
├── memory/          # Memórias do agente
│   └── 2026-02-14.md
└── google_ads_monitor.py  # Script de monitoramento
```

## Credenciais

Tokens OAuth: `/home/julio/.openclaw/workspace/google_oauth_tokens.json`

## Próximos Passos

1. [ ] Testar script de monitoramento
2. [ ] Configurar cron job para rodar diariamente às 08:00
3. [ ] Integrar com Notion DB
4. [ ] Criar relatórios automáticos
