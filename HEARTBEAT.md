# HEARTBEAT.md

# Add tasks below when you want the agent to check something periodically.

## Follow-up Lia (a cada 5 minutos)
Verificar novas tarefas adicionadas no banco de dados Notion "Follow-up Lia"
- Usar modelo local: ollama/qwen2.5:1.5b
- Checar se Julio adicionou tarefas novas
- Alertar sobre tarefas urgentes
- Atualizar status das tarefas em andamento

## Tarefas de Follow-up Lia
1. Verificar Notion DB "Follow-up Lia" por tarefas com tag "Lia"
2. Identificar tarefas novas (criadas desde último check)
3. Identificar tarefas urgentes/prioridade alta
4. Atualizar progresso de tarefas em andamento
5. Reportar summary no chat

## Lógica de Prioridade
- 🔴 Prioridade Alta / Urgente → Alertar imediatamente
- 🟡 Prioridade Média → Incluir no report
- 🟢 Prioridade Baixa → Só reportar se não houver urgentes

## Formato de Output
```
📋 FOLLOW-UP LIA

🆕 Novas Tarefas:
- [ ] Tarefa 1
- [ ] Tarefa 2

⚠️ Urgentes:
- [ ] Tarefa 3

📊 Em Andamento:
- [ ] Tarefa 4 (50%)

✅ Concluídas Recentemente:
- [ ] Tarefa 5
```

## Modelo a Usar
Para heartbeat: ollama/qwen2.5:1.5b (local, econômico)
