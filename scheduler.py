#!/usr/bin/env python3
"""
scheduler.py — Agenda commits automáticos ao longo do dia.
Rode com: python scheduler.py
"""

import schedule
import time
import random
import subprocess
import sys
from datetime import datetime

# ─── CONFIGURAÇÕES ────────────────────────────────────────────────
COMMITS_PER_DAY = 3          # Quantos commits por dia
START_HOUR = 9               # Hora mínima para commitar (9h)
END_HOUR = 22                # Hora máxima para commitar (22h)
REPO_PATH = "."              # Caminho do repositório (altere se necessário)
# ──────────────────────────────────────────────────────────────────

def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")

def run_commit():
    now = datetime.now()
    if not (START_HOUR <= now.hour < END_HOUR):
        log("⏸️  Fora do horário permitido, pulando...")
        return

    try:
        result = subprocess.run(
            [sys.executable, "auto_commit.py", "commit"],
            capture_output=True, text=True,
            cwd=REPO_PATH
        )
        log(result.stdout.strip() or "Commit realizado!")
        if result.stderr:
            log(f"⚠️  {result.stderr.strip()}")
    except Exception as e:
        log(f"❌ Erro: {e}")

def schedule_random_commits():
    """Distribui commits em horários aleatórios ao longo do dia."""
    schedule.clear()

    # Distribui os commits aleatoriamente no intervalo permitido
    hours_available = list(range(START_HOUR, END_HOUR))
    chosen_hours = sorted(random.sample(hours_available, min(COMMITS_PER_DAY, len(hours_available))))

    for hour in chosen_hours:
        minute = random.randint(0, 59)
        time_str = f"{hour:02d}:{minute:02d}"
        schedule.every().day.at(time_str).do(run_commit)
        log(f"📅 Commit agendado para {time_str}")

    # Reagenda todo dia à meia-noite para novos horários aleatórios
    schedule.every().day.at("00:01").do(schedule_random_commits)

if __name__ == "__main__":
    log("🚀 Scheduler iniciado!")
    log(f"⚙️  {COMMITS_PER_DAY} commits/dia entre {START_HOUR}h e {END_HOUR}h")
    schedule_random_commits()

    while True:
        schedule.run_pending()
        time.sleep(30)
