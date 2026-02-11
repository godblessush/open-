import os
import subprocess
import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import box

console = Console()

# Logo
logo = """
███████╗███████╗███╗   ██╗ ██████╗
╚══███╔╝██╔════╝████╗  ██║██╔════╝
  ███╔╝ █████╗  ██╔██╗ ██║██║     
 ███╔╝  ██╔══╝  ██║╚██╗██║██║     
███████╗███████╗██║ ╚████║╚██████╗
╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝
"""

console.print(Panel.fit(logo, title="[bold cyan]Z3NO Cyberpunk Terminal[/bold cyan]", border_style="bright_magenta"))

# Auto log setup
log_file = f"scan_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
def log_output(data):
    with open(log_file, 'a') as f:
        f.write(data + "\n")

# Categorize port strength
def categorize_port(port, service):
    weak_ports = {
        21: "FTP (no encryption)",
        23: "Telnet (insecure)",
        80: "HTTP (unencrypted)",
        445: "SMB (can be exploited)",
        139: "NetBIOS (legacy)"
    }
    strong_ports = {
        22: "SSH (encrypted)",
        443: "HTTPS",
        3306: "MySQL (requires creds)",
        3389: "RDP (can be secured)"
    }
    if port in weak_ports:
        return f"[red]Weak[/red] - {weak_ports[port]}"
    elif port in strong_ports:
        return f"[green]Strong[/green] - {strong_ports[port]}"
    else:
        return "[yellow]Unknown[/yellow]"

# Scan with nmap
def run_nmap():
    ip = Prompt.ask("[cyan]Enter IP to scan[/cyan]")
    command = ["nmap", "-A", ip]
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout
    log_output(output)

    # Parse and categorize ports
    console.print("\n[bold magenta]Scan Summary:[/bold magenta]\n")
    ports_found = []
    for line in output.splitlines():
        if "/tcp" in line and "open" in line:
            parts = line.split()
            port = int(parts[0].split("/")[0])
            service = parts[2] if len(parts) > 2 else "Unknown"
            category = categorize_port(port, service)
            console.print(f"Port {port} - {service} - {category}")
            ports_found.append((port, service))

    # Offer to open SSH or Web based on ports
    for port, service in ports_found:
        if port == 22:
            if Prompt.ask("[blue]SSH port open. Connect now? (y/n)[/blue]", choices=["y", "n"]) == "y":
                user = Prompt.ask("Enter SSH username")
                os.system(f"start cmd /k ssh {user}@{ip}")
        if port in [80, 443, 8080, 5357]:
            if Prompt.ask("[green]Web service detected. Open in browser? (y/n)[/green]", choices=["y", "n"]) == "y":
                os.system(f"start http://{ip}:{port}")

# Menu loop
while True:
    console.print("\n[bold cyan]Z3NO Command Menu[/bold cyan]", style="magenta")
    table = Table(box=box.ROUNDED)
    table.add_column("Option", style="cyan")
    table.add_column("Tool")
    table.add_row("1", "Run Nmap Scan")
    table.add_row("2", "Nikto (Coming Soon)")
    table.add_row("3", "Hydra (Coming Soon)")
    table.add_row("4", "Exit")
    console.print(table)

    choice = Prompt.ask("\n[bold yellow]Choose an option[/bold yellow]", choices=["1", "2", "3", "4"])

    if choice == "1":
        run_nmap()
    elif choice == "4":
        break
    else:
        console.print("[italic red]Feature not implemented yet.[/italic red]")