"""Geração de dados simulados de telemetria — MobilitySat-1."""

import random
from datetime import datetime


# Limites operacionais de cada parâmetro
LIMITES = {
    "drift_oscilador_ns": {
        "normal_max": 10,
        "atencao_max": 50,
        "unidade": "ns",
        "descricao": "Deriva do oscilador atômico"
    },
    "sincronizacao_constelacao": {
        "normal_min": 95,
        "atencao_min": 80,
        "unidade": "%",
        "descricao": "Sincronização com a constelação GPS/Galileo"
    },
    "integridade_sinal_l1_l5": {
        "normal_min": 98,
        "atencao_min": 90,
        "unidade": "%",
        "descricao": "Integridade do sinal L1/L5"
    },
    "precisao_efemeride_m": {
        "normal_max": 0.5,
        "atencao_max": 2.0,
        "unidade": "m",
        "descricao": "Precisão da efeméride"
    },
    "margem_potencia_w": {
        "normal_min": 50,
        "atencao_min": 15,
        "unidade": "W",
        "descricao": "Margem de potência disponível"
    },
}


def coletar(modo="normal"):
    """
    Gera dados simulados de telemetria do MobilitySat-1.

    Modos disponíveis:
    - 'normal'   : todos os parâmetros dentro do esperado
    - 'atencao'  : parâmetros em zona de atenção
    - 'critico'  : parâmetros em zona crítica
    - 'aleatorio': variação aleatória realista
    """

    if modo == "normal":
        dados = {
            "drift_oscilador_ns": round(random.uniform(1, 9), 2),
            "sincronizacao_constelacao": round(random.uniform(96, 99.9), 2),
            "integridade_sinal_l1_l5": round(random.uniform(98.5, 99.9), 2),
            "precisao_efemeride_m": round(random.uniform(0.1, 0.45), 3),
            "margem_potencia_w": round(random.uniform(55, 100), 1),
        }

    elif modo == "atencao":
        dados = {
            "drift_oscilador_ns": round(random.uniform(15, 45), 2),
            "sincronizacao_constelacao": round(random.uniform(81, 94), 2),
            "integridade_sinal_l1_l5": round(random.uniform(91, 97), 2),
            "precisao_efemeride_m": round(random.uniform(0.6, 1.9), 3),
            "margem_potencia_w": round(random.uniform(16, 49), 1),
        }

    elif modo == "critico":
        dados = {
            "drift_oscilador_ns": round(random.uniform(55, 120), 2),
            "sincronizacao_constelacao": round(random.uniform(50, 79), 2),
            "integridade_sinal_l1_l5": round(random.uniform(70, 89), 2),
            "precisao_efemeride_m": round(random.uniform(2.1, 5.0), 3),
            "margem_potencia_w": round(random.uniform(1, 14), 1),
        }

    else:  # aleatorio
        dados = {
            "drift_oscilador_ns": round(random.uniform(1, 120), 2),
            "sincronizacao_constelacao": round(random.uniform(50, 99.9), 2),
            "integridade_sinal_l1_l5": round(random.uniform(70, 99.9), 2),
            "precisao_efemeride_m": round(random.uniform(0.1, 5.0), 3),
            "margem_potencia_w": round(random.uniform(1, 100), 1),
        }

    dados["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dados["satelite"] = "MobilitySat-1"
    dados["orbita"] = "MEO — 20.200 km"

    return dados


def formatar(dados):
    """Formata os dados de telemetria em texto legível para o prompt."""
    return f"""
Telemetria — {dados['satelite']} ({dados['orbita']})
Timestamp: {dados['timestamp']}

- drift_oscilador_ns:       {dados['drift_oscilador_ns']} ns
- sincronizacao_constelacao: {dados['sincronizacao_constelacao']} %
- integridade_sinal_l1_l5:  {dados['integridade_sinal_l1_l5']} %
- precisao_efemeride_m:     {dados['precisao_efemeride_m']} m
- margem_potencia_w:        {dados['margem_potencia_w']} W
""".strip()