"""
Command-line interface for HotkeyForge.
"""

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from hotkeyforge import __version__
from hotkeyforge.constants import DEFAULT_TEMPLATES, SUPPORTED_PLATFORMS
from hotkeyforge.core import Hotkey, HotkeyConfig, HotkeyManager

console = Console()


def print_banner() -> None:
    """Print application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██╗  ██╗ ██████╗ ██████╗ ███████╗██╗  ██╗██╗   ██╗     ║
║   ██║  ██║██╔═══██╗██╔══██╗██╔════╝██║  ██║╚██╗ ██╔╝     ║
║   ███████║██║   ██║██║  ██║█████╗  ███████║ ╚████╔╝      ║
║   ██╔══██║██║   ██║██║  ██║██╔══╝  ██╔══██║  ╚██╔╝       ║
║   ██║  ██║╚██████╔╝██████╔╝███████╗██║  ██║   ██║        ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝        ║
║                                                           ║
║           🔥 Cross-Platform Hotkey Manager 🔥            ║
║                    Version: {version}                     ║
╚═══════════════════════════════════════════════════════════╝
""".format(version=__version__)
    
    console.print(banner, style="bold cyan")


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
@click.pass_context
def main(ctx: click.Context, version: bool) -> None:
    """HotkeyForge - A powerful cross-platform hotkey management CLI tool."""
    if version:
        console.print(f"HotkeyForge version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        print_banner()
        console.print("\nUse [bold]hotkeyforge --help[/bold] to see available commands.\n")


@main.command()
@click.option("--name", "-n", required=True, help="Hotkey name")
@click.option("--keys", "-k", required=True, help="Key combination (e.g., 'ctrl+alt+t')")
@click.option("--description", "-d", default="", help="Hotkey description")
@click.option("--action", "-a", type=click.Choice(["command", "script", "url", "custom"]), 
              default="command", help="Action type")
@click.option("--command", "-c", help="Command to execute")
@click.option("--script", "-s", help="Script path to execute")
@click.option("--url", "-u", help="URL to open")
@click.option("--profile", "-p", default="default", help="Profile name")
@click.option("--tags", "-t", help="Comma-separated tags")
def add(
    name: str,
    keys: str,
    description: str,
    action: str,
    command: Optional[str],
    script: Optional[str],
    url: Optional[str],
    profile: str,
    tags: Optional[str],
) -> None:
    """Add a new hotkey."""
    config = HotkeyConfig()
    
    if name in config.hotkeys:
        console.print(f"[red]Error: Hotkey '{name}' already exists.[/red]")
        sys.exit(1)
    
    hotkey = Hotkey(
        name=name,
        keys=keys,
        description=description,
        action=action,
        command=command,
        script=script,
        url=url,
        profile=profile,
        tags=tags.split(",") if tags else [],
    )
    
    if config.add_hotkey(hotkey):
        console.print(f"[green]✓ Hotkey '{name}' added successfully.[/green]")
        console.print(f"  Keys: [cyan]{keys}[/cyan]")
        console.print(f"  Action: [yellow]{action}[/yellow]")
    else:
        console.print(f"[red]Error: Failed to add hotkey '{name}'.[/red]")
        sys.exit(1)


@main.command()
@click.argument("name")
def remove(name: str) -> None:
    """Remove a hotkey."""
    config = HotkeyConfig()
    
    if config.remove_hotkey(name):
        console.print(f"[green]✓ Hotkey '{name}' removed successfully.[/green]")
    else:
        console.print(f"[red]Error: Hotkey '{name}' not found.[/red]")
        sys.exit(1)


@main.command()
@click.argument("name")
@click.option("--keys", "-k", help="New key combination")
@click.option("--description", "-d", help="New description")
@click.option("--command", "-c", help="New command")
@click.option("--enabled/--disabled", default=None, help="Enable or disable")
def update(
    name: str,
    keys: Optional[str],
    description: Optional[str],
    command: Optional[str],
    enabled: Optional[bool],
) -> None:
    """Update an existing hotkey."""
    config = HotkeyConfig()
    
    updates = {}
    if keys:
        updates["keys"] = keys
    if description is not None:
        updates["description"] = description
    if command:
        updates["command"] = command
    if enabled is not None:
        updates["enabled"] = enabled
    
    if config.update_hotkey(name, updates):
        console.print(f"[green]✓ Hotkey '{name}' updated successfully.[/green]")
    else:
        console.print(f"[red]Error: Hotkey '{name}' not found.[/red]")
        sys.exit(1)


@main.command("list")
@click.option("--profile", "-p", help="Filter by profile")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--enabled/--all", default=True, help="Show only enabled hotkeys")
def list_hotkeys(profile: Optional[str], tag: Optional[str], enabled: bool) -> None:
    """List all hotkeys."""
    config = HotkeyConfig()
    hotkeys = config.list_hotkeys(profile=profile)
    
    if enabled:
        hotkeys = [hk for hk in hotkeys if hk.enabled]
    
    if tag:
        hotkeys = [hk for hk in hotkeys if tag in hk.tags]
    
    if not hotkeys:
        console.print("[yellow]No hotkeys found.[/yellow]")
        return
    
    table = Table(title="📋 Hotkeys", show_header=True, header_style="bold cyan")
    table.add_column("Name", style="green")
    table.add_column("Keys", style="cyan")
    table.add_column("Action", style="yellow")
    table.add_column("Description", style="white")
    table.add_column("Status", style="magenta")
    table.add_column("Triggers", style="dim")
    
    for hk in hotkeys:
        status = "✓" if hk.enabled else "✗"
        status_style = "green" if hk.enabled else "red"
        table.add_row(
            hk.name,
            hk.keys,
            hk.action,
            hk.description or "-",
            f"[{status_style}]{status}[/{status_style}]",
            str(hk.trigger_count),
        )
    
    console.print(table)


@main.command()
def conflicts() -> None:
    """Detect hotkey conflicts."""
    config = HotkeyConfig()
    conflicts = config.detect_conflicts()
    
    if not conflicts:
        console.print("[green]✓ No conflicts detected.[/green]")
        return
    
    console.print("[red]⚠ Conflicts detected:[/red]\n")
    
    for keys, names in conflicts.items():
        console.print(f"  [yellow]{keys}[/yellow]:")
        for name in names:
            console.print(f"    - {name}")
    
    console.print("\n[yellow]Tip: Use 'hotkeyforge update' to change key combinations.[/yellow]")


@main.command()
def start() -> None:
    """Start the hotkey listener daemon."""
    manager = HotkeyManager()
    
    if manager.is_running():
        console.print("[yellow]Hotkey listener is already running.[/yellow]")
        return
    
    console.print("[cyan]Starting hotkey listener...[/cyan]")
    console.print("[dim]Press Ctrl+C to stop.[/dim]\n")
    
    manager.start()
    
    try:
        # Keep running
        import time
        while manager.is_running():
            time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Stopping hotkey listener...[/yellow]")
        manager.stop()
        console.print("[green]✓ Hotkey listener stopped.[/green]")


@main.command()
def stats() -> None:
    """Show hotkey usage statistics."""
    manager = HotkeyManager()
    statistics = manager.get_statistics()
    
    console.print(Panel.fit(
        f"[bold]Total Hotkeys:[/bold] {statistics['total_hotkeys']}\n"
        f"[bold]Enabled:[/bold] {statistics['enabled_hotkeys']}\n"
        f"[bold]Total Triggers:[/bold] {statistics['total_triggers']}",
        title="📊 Statistics",
        border_style="cyan",
    ))
    
    if statistics["hotkeys"]:
        table = Table(title="Hotkey Usage", show_header=True, header_style="bold cyan")
        table.add_column("Name", style="green")
        table.add_column("Triggers", style="yellow")
        table.add_column("Last Triggered", style="dim")
        
        for name, data in statistics["hotkeys"].items():
            last = data.get("last_triggered", "Never")
            if last and last != "Never":
                last = last.split("T")[0]  # Just show date
            table.add_row(name, str(data["trigger_count"]), last)
        
        console.print(table)


@main.command()
def templates() -> None:
    """List available hotkey templates."""
    console.print("[bold]Available Templates:[/bold]\n")
    
    for name, template in DEFAULT_TEMPLATES.items():
        console.print(f"  [cyan]{name}[/cyan]")
        console.print(f"    {template.get('description', 'No description')}")
        console.print(f"    Hotkeys: {len(template.get('hotkeys', {}))}")
        console.print()


@main.command()
@click.argument("template_name")
def apply(template_name: str) -> None:
    """Apply a hotkey template."""
    manager = HotkeyManager()
    
    if manager.apply_template(template_name):
        console.print(f"[green]✓ Template '{template_name}' applied successfully.[/green]")
    else:
        console.print(f"[red]Error: Template '{template_name}' not found.[/red]")
        console.print("\n[yellow]Available templates:[/yellow]")
        for name in DEFAULT_TEMPLATES.keys():
            console.print(f"  - {name}")
        sys.exit(1)


@main.command()
@click.argument("path", type=click.Path())
def export(path: str) -> None:
    """Export configuration to file."""
    manager = HotkeyManager()
    
    if manager.export_config(Path(path)):
        console.print(f"[green]✓ Configuration exported to '{path}'.[/green]")
    else:
        console.print(f"[red]Error: Failed to export configuration.[/red]")
        sys.exit(1)


@main.command()
@click.argument("path", type=click.Path(exists=True))
def import_config(path: str) -> None:
    """Import configuration from file."""
    manager = HotkeyManager()
    
    if manager.import_config(Path(path)):
        console.print(f"[green]✓ Configuration imported from '{path}'.[/green]")
    else:
        console.print(f"[red]Error: Failed to import configuration.[/red]")
        sys.exit(1)


@main.command()
@click.option("--show", is_flag=True, help="Show current settings")
@click.option("--auto-start/--no-auto-start", default=None, help="Enable/disable auto-start")
@click.option("--notifications/--no-notifications", default=None, help="Enable/disable notifications")
def config(show: bool, auto_start: Optional[bool], notifications: Optional[bool]) -> None:
    """Manage application settings."""
    cfg = HotkeyConfig()
    
    if show or (auto_start is None and notifications is None):
        settings = cfg.get_settings()
        console.print(Panel.fit(
            f"[bold]Auto Start:[/bold] {settings.get('auto_start', False)}\n"
            f"[bold]Notifications:[/bold] {settings.get('show_notifications', True)}\n"
            f"[bold]Log Enabled:[/bold] {settings.get('log_enabled', True)}\n"
            f"[bold]Conflict Detection:[/bold] {settings.get('conflict_detection', True)}\n"
            f"[bold]Stats Enabled:[/bold] {settings.get('stats_enabled', True)}",
            title="⚙️ Settings",
            border_style="cyan",
        ))
        return
    
    updates = {}
    if auto_start is not None:
        updates["auto_start"] = auto_start
    if notifications is not None:
        updates["show_notifications"] = notifications
    
    if updates:
        cfg.update_settings(updates)
        console.print("[green]✓ Settings updated.[/green]")


@main.command()
def info() -> None:
    """Show system and application information."""
    import platform
    
    console.print(Panel.fit(
        f"[bold]HotkeyForge[/bold] v{__version__}\n\n"
        f"[bold]Platform:[/bold] {platform.system()} {platform.release()}\n"
        f"[bold]Python:[/bold] {platform.python_version()}\n"
        f"[bold]Config Path:[/bold] {HotkeyConfig().config_path}\n"
        f"[bold]Log Path:[/bold] ~/.local/share/hotkeyforge/hotkeyforge.log\n"
        f"[bold]Supported Platforms:[/bold] {', '.join(SUPPORTED_PLATFORMS)}",
        title="ℹ️ System Information",
        border_style="cyan",
    ))


if __name__ == "__main__":
    main()
