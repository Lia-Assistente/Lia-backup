#!/usr/bin/env python3
"""
Drive Journal Cleanup - Mantém apenas o arquivo mais recente
Remove arquivos antigos baseados em padrão de data (DD-MM-AAAA ou YYYY-MM-DD)
"""
import os
import glob
import re
import shutil
from pathlib import Path

def extract_date_from_filename(filename):
    """Extrai data do nome do arquivo para ordenação"""
    # Padrão brasileiro: DD-MM-AAAA
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})', filename)
    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"
    
    # Padrão ISO: AAAA-MM-DD
    match = re.search(r'(\d{4})-(\d{2})-(\d{2})', filename)
    if match:
        return match.group(0)
    
    return None

def cleanup_journal_files(directory, patterns=None):
    """Remove arquivos antigos, mantendo apenas o mais recente"""
    if patterns is None:
        patterns = [
            "*Diary*",
            "*diary*", 
            "*Diário*",
            "*diário*",
            "*Journal*",
            "*journal*",
        ]
    
    all_files = []
    
    for pattern in patterns:
        all_files.extend(glob.glob(os.path.join(directory, pattern)))
        all_files.extend(glob.glob(os.path.join(directory, "**", pattern), recursive=True))
    
    # Remove duplicatas
    all_files = list(set(all_files))
    
    # Filtra apenas arquivos (não diretórios) e extrai datas
    file_dates = []
    for filepath in all_files:
        if os.path.isfile(filepath):
            date_str = extract_date_from_filename(os.path.basename(filepath))
            if date_str:
                file_dates.append((filepath, date_str))
    
    if len(file_dates) <= 1:
        return {"status": "nothing_to_clean", "message": "0 ou 1 arquivo encontrado"}
    
    # Ordena por data (mais recente primeiro)
    file_dates.sort(key=lambda x: x[1], reverse=True)
    
    # Mantém o mais recente, remove os outros
    newest = file_dates[0]
    removed = file_dates[1:]
    
    for filepath, date_str in removed:
        os.remove(filepath)
    
    return {
        "status": "success",
        "kept": newest[0],
        "removed_count": len(removed),
        "removed_files": [f[0] for f in removed]
    }

if __name__ == "__main__":
    workspace = "/home/julio/.openclaw/workspace"
    result = cleanup_journal_files(workspace)
    print(result)
