"""Banner ASCII da Mission Control AI — MobilitySat."""

import argparse
import pyfiglet
from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

FONTES_DEMO = ["ansi_shadow", "slant", "big", "banner3-D", "doom", "epic", "isometric1", "larry3d"]


def mostrar_banner(font="ansi_shadow"):
    linha1 = pyfiglet.figlet_format("Global Solution 2026.1", font=font)
    linha2 = pyfiglet.figlet_format("Mission Control AI", font=font)
    console.print(Align.center(Text(linha1, style="bold #A855F7")))
    console.print(Align.center(Text(linha2, style="bold #06B6D4")))
    console.print(Align.center(
        Text("── 2026.1 · Prompt Engineering and AI · FIAP ──",
             style="italic #8484A0")
    ))
    console.print(Align.center(
        Text("🚗 MobilitySat — GNSS e Mobilidade",
             style="bold #F59E0B")
    ))


def listar_fontes():
    fontes = pyfiglet.FigletFont.getFonts()
    console.print(f"[bold]Total de fontes disponíveis: {len(fontes)}[/bold]")
    for f in sorted(fontes):
        console.print(f"  {f}")


def demo_fontes():
    for font in FONTES_DEMO:
        console.rule(f"[bold cyan]{font}[/bold cyan]")
        try:
            texto = pyfiglet.figlet_format("MobilitySat", font=font)
            console.print(Text(texto, style="bold #06B6D4"))
        except Exception:
            console.print(f"[red]Fonte {font} indisponível[/red]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerador de banner ASCII — Mission Control AI")
    parser.add_argument("-fonts", action="store_true", help="Lista todas as fontes disponíveis")
    parser.add_argument("-font", type=str, default="ansi_shadow", help="Fonte a usar no banner")
    parser.add_argument("-text", type=str, default=None, help="Texto customizado para exibir")
    parser.add_argument("-demo", action="store_true", help="Demonstra 8 fontes lado a lado")
    args = parser.parse_args()

    if args.fonts:
        listar_fontes()
    elif args.demo:
        demo_fontes()
    elif args.text:
        texto = pyfiglet.figlet_format(args.text, font=args.font)
        console.print(Text(texto, style="bold #06B6D4"))
    else:
        mostrar_banner(font=args.font)