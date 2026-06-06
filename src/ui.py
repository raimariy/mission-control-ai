"""Interface CLI estilo Claude Code — usa Rich + prompt-toolkit."""

import pyfiglet
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style

console = Console()
session = PromptSession(style=Style.from_dict({"prompt": "#06B6D4 bold"}))


def show_banner():
    """Exibe banner ASCII colorido no início."""
    linha1 = pyfiglet.figlet_format("Mission Control", font="ansi_shadow")
    linha2 = pyfiglet.figlet_format("MobilitySat", font="ansi_shadow")
    console.print(Text(linha1, style="bold #06B6D4"))
    console.print(Text(linha2, style="bold #F59E0B"))
    console.print(Panel.fit(
        "🚗 Satélite GNSS de Navegação — MobilitySat-1\n"
        "Sistema de monitoramento e análise por IA generativa.\n"
        "Use [bold]/help[/bold] para ver os comandos · [bold]/exit[/bold] para sair.\n"
        "Modelo: gpt-oss:120b via Ollama Cloud",
        title="◆ MISSION CONTROL AI",
        border_style="#06B6D4"
    ))


def show_response(text):
    """Renderiza resposta da IA em painel com timestamp."""
    now = datetime.now().strftime("%H:%M")
    console.print(Panel(
        text,
        title="◆ ARIA — Mission Control",
        subtitle=now,
        border_style="#06B6D4"
    ))


def show_help():
    """Exibe tabela de comandos disponíveis."""
    table = Table(title="Comandos disponíveis", border_style="#06B6D4")
    table.add_column("Comando", style="#F59E0B bold")
    table.add_column("Descrição")
    table.add_row("/help", "Exibe esta tabela de comandos")
    table.add_row("/status", "Mostra snapshot atual da telemetria")
    table.add_row("/about", "Informações sobre o projeto e o grupo")
    table.add_row("/clear", "Limpa o terminal e reexibe o banner")
    table.add_row("/exit", "Encerra o sistema")
    table.add_row("[qualquer texto]", "Envia pergunta para análise da IA")
    console.print(table)


def show_about():
    """Exibe informações sobre o projeto."""
    console.print(Panel.fit(
        "🚀 [bold]Mission Control AI — MobilitySat[/bold]\n\n"
        "Trilha: 🚗 MobilitySat — GNSS e Mobilidade\n"
        "Satélite simulado: MobilitySat-1 (GNSS MEO)\n"
        "Impacto terrestre: frotas logísticas, agricultura de precisão,\n"
        "veículos autônomos.\n\n"
        "Disciplina: Prompt Engineering and Artificial Intelligence\n"
        "FIAP · Ciência da Computação · Global Solution 2026.1",
        title="◆ Sobre o Projeto",
        border_style="#A855F7"
    ))


def run_cli(engine):
    """Loop principal da CLI."""
    show_banner()

    if not engine.is_ready():
        console.print(
            "  ⚠ Engine status: AGUARDANDO IMPLEMENTAÇÃO ✗\n",
            style="yellow"
        )

    while True:
        try:
            user_input = session.prompt("❯ ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[bold #06B6D4]Encerrando Mission Control AI. Até logo![/bold #06B6D4]")
            break

        if not user_input:
            continue

        if user_input == "/exit":
            console.print("[bold #06B6D4]Encerrando Mission Control AI. Até logo![/bold #06B6D4]")
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/about":
            show_about()
            continue

        if user_input == "/status":
            show_response(engine.status_snapshot())
            continue

        if user_input == "/clear":
            console.clear()
            show_banner()
            continue

        # Qualquer outra entrada vai para o motor de análise
        console.print("  [dim]Consultando ARIA...[/dim]")
        resposta = engine.analyze(user_input)
        show_response(resposta)