"""Motor de análise da Mission Control AI."""

import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TRILHA = "mobilitysat"

client = Client(
    host="https://ollama.com",
    headers={'Authorization': 'Bearer ' + os.environ.get('OLLAMA_API_KEY', '')}
)


def llm(prompt, system=None, max_tokens=800, temperature=0.3):
    """Envia prompt ao gpt-oss:120b via Ollama Cloud."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    try:
        return client.chat(
            model="gpt-oss:120b",
            messages=messages,
            options={"num_predict": max_tokens, "temperature": temperature},
            stream=False
        )['message']['content'].strip()
    except Exception as e:
        return f"⚠️ Erro ao consultar IA: {e}"


def load_system_prompt():
    """Lê o system prompt do arquivo prompts/system_prompt.md"""
    path = Path("prompts/system_prompt.md")
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "Você é um assistente."


class MissionEngine:
    """Motor de análise — métodos serão completados nas próximas etapas."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()

    def is_ready(self):
        # Trocamos para True quando analyze() estiver implementado
        return False

    def status_snapshot(self):
        """Retorna texto resumindo o estado atual da telemetria."""
        return "🛠 status_snapshot() ainda não implementado."

    def analyze(self, pergunta_usuario):
        """Analisa a pergunta com base na telemetria + alertas + IA."""
        return (
            "🛠 Implementação pendente.\n\n"
            "Olá! A interface CLI está funcionando, mas a lógica\n"
            "de análise ainda não foi conectada. O grupo precisa:\n\n"
            " 1. Completar src/telemetria.py\n"
            " 2. Completar src/alertas.py\n"
            " 3. Escrever o system prompt em prompts/system_prompt.md\n"
            " 4. Sobrescrever analyze() em src/engine.py"
        )