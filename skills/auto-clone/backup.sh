#!/bin/bash
# Auto backup script for Lia-backup
# Run via cron every 2 hours

REPO_DIR="/home/julio/.openclaw/workspace"
BRANCH="main"

cd "$REPO_DIR" || exit 1

# Check if there are changes
if git diff --quiet && git diff --staged --quiet; then
    echo "Sem alterações para fazer backup."
    exit 0
fi

echo "→ Fazendo backup..."

# Add all changes
git add -A

# Commit with timestamp
git commit -m "Backup $(date '+%Y-%m-%d %H:%M')"

# Push to remote
git push origin "$BRANCH"

echo "✓ Backup enviado para Lia-backup"
echo "---"
echo "Última execução: $(date)"
