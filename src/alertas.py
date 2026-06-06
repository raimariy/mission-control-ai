"""Lógica de alertas e decisão — MobilitySat-1."""


# Thresholds operacionais
THRESHOLDS = {
    "drift_oscilador_ns": {"atencao": 10, "critico": 50},
    "sincronizacao_constelacao": {"atencao": 95, "critico": 80},
    "integridade_sinal_l1_l5": {"atencao": 98, "critico": 90},
    "precisao_efemeride_m": {"atencao": 0.5, "critico": 2.0},
    "margem_potencia_w": {"atencao": 50, "critico": 15},
}


def classificar_parametro(nome, valor):
    """
    Classifica um parâmetro como 'nominal', 'atencao' ou 'critico'.
    Retorna tupla (status, mensagem).
    """
    t = THRESHOLDS[nome]

    # Parâmetros onde valor ALTO é ruim
    if nome in ["drift_oscilador_ns", "precisao_efemeride_m"]:
        if valor >= t["critico"]:
            return "critico", f"{nome} em {valor} — ACIMA do limite crítico ({t['critico']})"
        elif valor >= t["atencao"]:
            return "atencao", f"{nome} em {valor} — ACIMA do limite de atenção ({t['atencao']})"
        else:
            return "nominal", f"{nome} em {valor} — nominal"

    # Parâmetros onde valor BAIXO é ruim
    else:
        if valor <= t["critico"]:
            return "critico", f"{nome} em {valor} — ABAIXO do limite crítico ({t['critico']})"
        elif valor <= t["atencao"]:
            return "atencao", f"{nome} em {valor} — ABAIXO do limite de atenção ({t['atencao']})"
        else:
            return "nominal", f"{nome} em {valor} — nominal"


def avaliar(dados):
    """
    Avalia todos os parâmetros da telemetria.
    Retorna dicionário com status geral e lista de alertas.
    """
    alertas = []
    status_geral = "nominal"

    parametros = [
        "drift_oscilador_ns",
        "sincronizacao_constelacao",
        "integridade_sinal_l1_l5",
        "precisao_efemeride_m",
        "margem_potencia_w",
    ]

    for param in parametros:
        if param not in dados:
            continue

        status, mensagem = classificar_parametro(param, dados[param])
        alertas.append({"parametro": param, "status": status, "mensagem": mensagem})

        # Status geral assume o pior entre todos os parâmetros
        if status == "critico":
            status_geral = "critico"
        elif status == "atencao" and status_geral == "nominal":
            status_geral = "atencao"

    # Respostas automatizadas para situações críticas
    acoes_automaticas = _acoes_automaticas(dados, alertas)

    return {
        "status_geral": status_geral,
        "alertas": alertas,
        "acoes_automaticas": acoes_automaticas,
    }


def _acoes_automaticas(dados, alertas):
    """
    Dispara respostas automatizadas para situações críticas.
    Lógica implementada em Python — não delegada à IA.
    """
    acoes = []

    # Ação 1 — potência crítica: ativar modo economia
    if dados.get("margem_potencia_w", 100) <= THRESHOLDS["margem_potencia_w"]["critico"]:
        acoes.append("⚡ AÇÃO AUTOMÁTICA: Modo economia de energia ativado — payload secundário desligado.")

    # Ação 2 — drift crítico do oscilador: acionar equipe de solo
    if dados.get("drift_oscilador_ns", 0) >= THRESHOLDS["drift_oscilador_ns"]["critico"]:
        acoes.append("🕐 AÇÃO AUTOMÁTICA: Alerta enviado à equipe de controle de solo — diagnóstico do oscilador necessário.")

    # Ação 3 — sincronização crítica: emitir aviso para operadores
    if dados.get("sincronizacao_constelacao", 100) <= THRESHOLDS["sincronizacao_constelacao"]["critico"]:
        acoes.append("📡 AÇÃO AUTOMÁTICA: NOTAM emitido — operadores de frota e agricultura notificados sobre degradação do sinal.")

    # Ação 4 — integridade crítica: suspender serviço de veículos autônomos
    if dados.get("integridade_sinal_l1_l5", 100) <= THRESHOLDS["integridade_sinal_l1_l5"]["critico"]:
        acoes.append("🚗 AÇÃO AUTOMÁTICA: Serviço de posicionamento para veículos autônomos suspenso por segurança.")

    # Ação 5 — precisão crítica: degradar nível de serviço
    if dados.get("precisao_efemeride_m", 0) >= THRESHOLDS["precisao_efemeride_m"]["critico"]:
        acoes.append("📍 AÇÃO AUTOMÁTICA: Nível de serviço rebaixado para padrão — agricultura de precisão centimétrica suspensa.")

    return acoes


def formatar_alertas(resultado):
    """Formata o resultado da avaliação em texto para injetar no prompt."""
    linhas = []

    status = resultado["status_geral"].upper()
    emoji = {"NOMINAL": "🟢", "ATENCAO": "🟡", "CRITICO": "🔴"}.get(status, "⚪")
    linhas.append(f"Status geral da missão: {emoji} {status}\n")

    linhas.append("Avaliação por parâmetro:")
    for alerta in resultado["alertas"]:
        e = {"nominal": "✅", "atencao": "⚠️", "critico": "🚨"}.get(alerta["status"], "•")
        linhas.append(f"  {e} {alerta['mensagem']}")

    if resultado["acoes_automaticas"]:
        linhas.append("\nAções automáticas disparadas:")
        for acao in resultado["acoes_automaticas"]:
            linhas.append(f"  {acao}")

    return "\n".join(linhas)