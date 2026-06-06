"""Motor de análise da Mission Control AI."""

import os
from ollama import Client
from dotenv import load_dotenv
from pathlib import Path
from src import telemetria, alertas

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
    """Motor de análise da Mission Control AI — MobilitySat."""

    def __init__(self):
        self.trilha = TRILHA
        self.system_prompt = load_system_prompt()
        self.historico = []  # memória dos últimos ciclos
        self.modo_telemetria = "aleatorio"  # modo padrão

    def is_ready(self):
        return True

    def status_snapshot(self):
        """Coleta telemetria, avalia alertas e retorna snapshot formatado."""
        dados = telemetria.coletar(modo=self.modo_telemetria)
        resultado = alertas.avaliar(dados)

        telemetria_txt = telemetria.formatar(dados)
        alertas_txt = alertas.formatar_alertas(resultado)

        return f"{telemetria_txt}\n\n{alertas_txt}"

    def analyze(self, pergunta_usuario):
        """
        Analisa a pergunta com base na telemetria + alertas + IA.
        1. Coleta dados via telemetria.coletar()
        2. Avalia alertas via alertas.avaliar()
        3. Monta prompt com dados + alertas + histórico + pergunta
        4. Chama llm() com o system prompt
        5. Armazena no histórico e retorna resposta
        """

        # Detecta se usuário quer mudar o modo de telemetria
        pergunta_lower = pergunta_usuario.lower()
        if "modo normal" in pergunta_lower:
            self.modo_telemetria = "normal"
        elif "modo atenção" in pergunta_lower or "modo atencao" in pergunta_lower:
            self.modo_telemetria = "atencao"
        elif "modo crítico" in pergunta_lower or "modo critico" in pergunta_lower:
            self.modo_telemetria = "critico"
        elif "modo aleatório" in pergunta_lower or "modo aleatorio" in pergunta_lower:
            self.modo_telemetria = "aleatorio"

        # 1. Coletar telemetria
        dados = telemetria.coletar(modo=self.modo_telemetria)

        # 2. Avaliar alertas
        resultado = alertas.avaliar(dados)

        # 3. Formatar dados e alertas
        telemetria_txt = telemetria.formatar(dados)
        alertas_txt = alertas.formatar_alertas(resultado)

        # 4. Montar histórico dos últimos 3 ciclos
        historico_txt = ""
        if self.historico:
            historico_txt = "\n\nHistórico recente (últimos ciclos):\n"
            for h in self.historico[-3:]:
                historico_txt += f"- [{h['timestamp']}] Status: {h['status_geral']}\n"

        # 5. Montar prompt completo
        prompt = f"""
{telemetria_txt}

{alertas_txt}
{historico_txt}

Pergunta do operador: {pergunta_usuario}
""".strip()

        # 6. Chamar IA
        resposta = llm(prompt, system=self.system_prompt)

        # 7. Salvar no histórico
        self.historico.append({
            "timestamp": dados["timestamp"],
            "status_geral": resultado["status_geral"],
            "pergunta": pergunta_usuario,
        })

        return resposta