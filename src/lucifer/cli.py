"""Command-line interface for Lucifer."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import click
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from lucifer import __version__
from lucifer.automation.workflows import WorkflowManager
from lucifer.core.assistant import LuciferAssistant
from lucifer.core.config import Config, get_config
from lucifer.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def print_banner():
    """Print Lucifer ASCII banner."""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ██╗     ██╗   ██╗ ██████╗██╗███████╗███████╗██████╗   ║
    ║   ██║     ██║   ██║██╔════╝██║██╔════╝██╔════╝██╔══██╗  ║
    ║   ██║     ██║   ██║██║     ██║█████╗  █████╗  ██████╔╝  ║
    ║   ██║     ██║   ██║██║     ██║██╔══╝  ██╔══╝  ██╔══██╗  ║
    ║   ███████╗╚██████╔╝╚██████╗██║██║     ███████╗██║  ██║  ║
    ║   ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝  ║
    ║                                                           ║
    ║        AI-Powered Cybersecurity Automation Assistant     ║
    ║                    Version """ + __version__ + """                      ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    console.print(banner, style="bold red")
    
    # Credits and donation info
    console.print("\n")
    credits_panel = Panel(
        "[bold cyan]Created by Yashab Alam[/bold cyan]\n\n"
        "[dim]LinkedIn:[/dim] [blue]linkedin.com/in/yashab-alam[/blue]\n"
        "[dim]Instagram:[/dim] [magenta]@yashab.alam[/magenta]\n"
        "[dim]Email:[/dim] yashabalam9@gmail.com\n\n"
        "[yellow]💖 Support this project:[/yellow] [green]Type 'donate' for details[/green]",
        title="[bold red]About[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    console.print(credits_panel)
    console.print("")


@click.group()
@click.version_option(version=__version__)
@click.option("--config", type=click.Path(exists=True), help="Config file path")
def cli(config: Optional[str]):
    """Lucifer - AI-powered cybersecurity automation assistant."""
    if config:
        # Load custom config
        pass


@cli.command()
def donate():
    """Show donation information to support the project."""
    console.print("\n")
    donation_panel = Panel(
        "[bold yellow]💖 Support Lucifer Development[/bold yellow]\n\n"
        "[green]Thank you for considering supporting this project![/green]\n\n"
        "[bold cyan]Created by Yashab Alam[/bold cyan]\n"
        "[dim]Contact:[/dim] yashabalam9@gmail.com\n\n"
        "[bold]Cryptocurrency Donations:[/bold]\n"
        "• Bitcoin (BTC): Contact for address\n"
        "• Ethereum (ETH): Contact for address\n"
        "• USDT (TRC20/ERC20): Contact for address\n"
        "• Other cryptocurrencies: Email me\n\n"
        "[bold]GitHub Sponsors:[/bold]\n"
        "• github.com/sponsors/yashab-cyber\n\n"
        "[bold]Connect with me:[/bold]\n"
        "• LinkedIn: linkedin.com/in/yashab-alam\n"
        "• Instagram: @yashab.alam\n"
        "• Email: yashabalam9@gmail.com\n\n"
        "[dim]Your support helps maintain and improve Lucifer!\n"
        "See DONATE.md for more details.[/dim]",
        title="[bold red]❤️  Donate[/bold red]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(donation_panel)
    console.print("\n")


@cli.command()
@click.option("--target", "-t", help="Target IP or domain")
@click.option("--workflow", "-w", help="Workflow to execute")
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
def start(target: Optional[str], workflow: Optional[str], interactive: bool):
    """Start Lucifer assistant."""
    print_banner()

    # Validate configuration
    config = get_config()
    if not config.validate_ai_credentials():
        console.print("[red]Error: AI credentials not configured[/red]")
        console.print("Please set up your .env file with API keys")
        sys.exit(1)

    console.print("[green]Initializing Lucifer...[/green]\n")

    # Run async main
    if interactive:
        asyncio.run(interactive_mode())
    elif workflow and target:
        asyncio.run(run_workflow_mode(target, workflow))
    else:
        console.print("[yellow]Use --interactive for interactive mode or specify --target and --workflow[/yellow]")
        console.print("\nExample: lucifer start -t 192.168.1.100 -w recon")


async def interactive_mode():
    """Run Lucifer in interactive mode."""
    assistant = LuciferAssistant()

    try:
        # Start terminal monitoring
        await assistant.start_terminal_monitoring()

        console.print("[green]Lucifer is now running in interactive mode[/green]")
        console.print("[dim]Type 'help' for available commands, 'exit' to quit[/dim]\n")

        # Set up command completion
        commands = [
            "help",
            "analyze",
            "suggest",
            "execute",
            "workflow",
            "record",
            "stop-record",
            "report",
            "donate",
            "credits",
            "exit",
        ]
        completer = WordCompleter(commands, ignore_case=True)
        session = PromptSession(completer=completer)

        while True:
            try:
                user_input = await asyncio.to_thread(
                    session.prompt, "lucifer> "
                )
                user_input = user_input.strip()

                if not user_input:
                    continue

                if user_input == "exit":
                    break
                elif user_input == "help":
                    show_help()
                elif user_input == "donate":
                    show_donate_info()
                elif user_input == "credits":
                    show_credits()
                elif user_input == "analyze":
                    await assistant.analyze_current_state()
                elif user_input == "suggest":
                    await assistant.suggest_next_actions()
                elif user_input.startswith("execute "):
                    cmd = user_input[8:]
                    await assistant.execute_command(cmd)
                elif user_input.startswith("workflow "):
                    parts = user_input.split()
                    if len(parts) >= 3:
                        workflow_name = parts[1]
                        target = parts[2]
                        await run_workflow(assistant, workflow_name, target)
                    else:
                        console.print("[yellow]Usage: workflow <name> <target>[/yellow]")
                elif user_input == "record":
                    assistant.start_recording()
                elif user_input == "stop-record":
                    assistant.stop_recording()
                elif user_input == "report":
                    await assistant.generate_report()
                else:
                    console.print(f"[yellow]Unknown command: {user_input}[/yellow]")

            except KeyboardInterrupt:
                continue
            except EOFError:
                break

    finally:
        assistant.stop()
        console.print("\n[green]Lucifer terminated[/green]")
        
        # Show donation reminder on exit
        console.print("\n")
        exit_panel = Panel(
            "[yellow]💖 Enjoyed using Lucifer?[/yellow]\n\n"
            "Support development by typing: [green]lucifer donate[/green]\n"
            "Or visit: [blue]github.com/yashab-cyber/lucifer[/blue]\n\n"
            "[dim]Created with ❤️ by Yashab Alam[/dim]",
            title="[bold red]Thank You![/bold red]",
            border_style="yellow",
            padding=(1, 2)
        )
        console.print(exit_panel)


async def run_workflow_mode(target: str, workflow_name: str):
    """Run a specific workflow."""
    assistant = LuciferAssistant()

    try:
        await assistant.start_terminal_monitoring()
        await run_workflow(assistant, workflow_name, target)
        await assistant.generate_report()
    finally:
        assistant.stop()


async def run_workflow(assistant: LuciferAssistant, workflow_name: str, target: str):
    """Execute a workflow."""
    console.print(f"\n[cyan]Executing {workflow_name} workflow on {target}[/cyan]\n")

    workflow_manager = WorkflowManager(
        assistant.ai_engine,
        assistant.terminal_capture,
    )

    context = {"target": target, "ports": "80,443"}
    results = await workflow_manager.execute_workflow(workflow_name, context)

    console.print("\n[green]Workflow completed![/green]")


def show_help():
    """Show help information."""
    table = Table(title="Lucifer Commands", show_header=True, header_style="bold cyan")
    table.add_column("Command", style="yellow")
    table.add_column("Description")

    commands_help = [
        ("help", "Show this help message"),
        ("analyze", "Analyze current terminal and screen state"),
        ("suggest", "Get AI suggestions for next actions"),
        ("execute <cmd>", "Execute a command in the monitored terminal"),
        ("workflow <name> <target>", "Run a pentesting workflow"),
        ("record", "Start screen recording"),
        ("stop-record", "Stop screen recording"),
        ("report", "Generate penetration testing report"),
        ("donate", "Show donation information"),
        ("credits", "Show creator credits"),
        ("exit", "Exit Lucifer"),
    ]

    for cmd, desc in commands_help:
        table.add_row(cmd, desc)

    console.print(table)

    console.print("\n[bold]Available Workflows:[/bold]")
    console.print("  • recon      - Reconnaissance and enumeration")
    console.print("  • webapp     - Web application testing")
    console.print("  • exploit    - Vulnerability exploitation")
    console.print("  • privesc    - Privilege escalation")


def show_donate_info():
    """Show donation information."""
    console.print("\n")
    donation_panel = Panel(
        "[bold yellow]💖 Support Lucifer Development[/bold yellow]\n\n"
        "[green]Thank you for considering supporting this project![/green]\n\n"
        "[bold cyan]Created by Yashab Alam[/bold cyan]\n"
        "[dim]Contact:[/dim] yashabalam9@gmail.com\n\n"
        "[bold]Cryptocurrency Donations:[/bold]\n"
        "• Bitcoin (BTC): Contact for address\n"
        "• Ethereum (ETH): Contact for address\n"
        "• USDT (TRC20/ERC20): Contact for address\n"
        "• Other cryptocurrencies: Email me\n\n"
        "[bold]GitHub Sponsors:[/bold]\n"
        "• github.com/sponsors/yashab-cyber\n\n"
        "[bold]Connect:[/bold]\n"
        "• LinkedIn: linkedin.com/in/yashab-alam\n"
        "• Instagram: @yashab.alam\n"
        "• Email: yashabalam9@gmail.com\n\n"
        "[dim]Your support helps maintain and improve Lucifer![/dim]",
        title="[bold red]❤️  Donate[/bold red]",
        border_style="yellow",
        padding=(1, 2)
    )
    console.print(donation_panel)
    console.print("\n")


def show_credits():
    """Show creator credits."""
    console.print("\n")
    credits_panel = Panel(
        "[bold red]LUCIFER[/bold red]\n"
        "[dim]AI-Powered Cybersecurity Automation Assistant[/dim]\n\n"
        "[bold cyan]Created by Yashab Alam[/bold cyan]\n\n"
        "[bold]Connect:[/bold]\n"
        "• LinkedIn: [blue]linkedin.com/in/yashab-alam[/blue]\n"
        "• Instagram: [magenta]@yashab.alam[/magenta]\n"
        "• GitHub: [green]github.com/yashab-cyber[/green]\n"
        "• Email: yashabalam9@gmail.com\n\n"
        "[yellow]💖 Support this project:[/yellow] [green]lucifer donate[/green]\n\n"
        "[dim]Open source • MIT License • Made with ❤️[/dim]",
        title="[bold red]Credits[/bold red]",
        border_style="red",
        padding=(1, 2)
    )
    console.print(credits_panel)
    console.print("\n")


@cli.command()
def workflows():
    """List available workflows."""
    console.print("\n[bold cyan]Available Pentesting Workflows[/bold cyan]\n")

    workflows_info = [
        ("recon", "Reconnaissance", "Comprehensive target reconnaissance and enumeration"),
        ("webapp", "Web Application Testing", "Automated web vulnerability assessment"),
        ("exploit", "Exploitation", "Automated vulnerability exploitation"),
        ("privesc", "Privilege Escalation", "Privilege escalation enumeration"),
    ]

    for name, title, desc in workflows_info:
        console.print(Panel(
            f"[yellow]{title}[/yellow]\n{desc}",
            title=f"[bold]{name}[/bold]",
            border_style="cyan",
        ))


@cli.command()
@click.argument("target")
def quick_scan(target: str):
    """Quick reconnaissance scan of target."""
    print_banner()
    console.print(f"\n[cyan]Running quick scan on {target}...[/cyan]\n")

    assistant = LuciferAssistant()

    try:
        asyncio.run(_quick_scan(assistant, target))
    finally:
        assistant.stop()


async def _quick_scan(assistant: LuciferAssistant, target: str):
    """Perform quick scan."""
    await assistant.start_terminal_monitoring()
    results = await assistant.run_automated_recon(target)

    console.print("\n[green]Quick scan completed![/green]")
    console.print(f"\nResults saved to: {assistant.config.report_dir}")


@cli.command()
def config_check():
    """Check configuration and credentials."""
    console.print("\n[bold cyan]Configuration Check[/bold cyan]\n")

    config = get_config()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Setting", style="yellow")
    table.add_column("Value")
    table.add_column("Status", style="green")

    # Check AI provider
    table.add_row(
        "AI Provider",
        config.ai_provider.value,
        "✓" if config.validate_ai_credentials() else "✗ Missing API key",
    )

    # Check directories
    table.add_row("Log Directory", str(config.log_file.parent), "✓" if config.log_file.parent.exists() else "✗")
    table.add_row("Report Directory", str(config.report_dir), "✓" if config.report_dir.exists() else "✗")

    # Check settings
    table.add_row("OCR Enabled", str(config.ocr_enabled), "✓")
    table.add_row("Audit Logging", str(config.audit_log_enabled), "✓")

    console.print(table)

    if not config.validate_ai_credentials():
        console.print("\n[red]⚠ Warning: AI credentials not configured[/red]")
        console.print("Please set up your .env file with the appropriate API keys")


def main():
    """Main entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        logger.exception("Fatal error")
        sys.exit(1)


if __name__ == "__main__":
    main()
