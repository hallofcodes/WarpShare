import os
import typer
from server import create_app
from waitress import serve
from rich.console import Console
from helpers.tunnel import start_tunnel
from utils.network_ip import get_local_ip
from utils.secrets_filter import confirm_to_share_secrets_in_cwd

# Initialize Typer and Rich console for clean formatting
cli = typer.Typer(
   name="WarpShare",
   help="⚡ Instant file sharing CLI tool (Local Wi-Fi & Remote Internet) ⚡",
   add_completion=False,
)
console = Console()



def start_server(host: str, port: int):
   app = create_app()
   serve(app, host=host, port=port)

# LOCAL SHARE

@cli.command(name="local")
def local_share(
   path: str = typer.Argument(os.getcwd(), help="The directory path or file to share"),
   port: int = typer.Option(3301, "--port", "-p", help="Port to run the local server on"),
):
   """
   Share files instantly with anyone on your local Wi-Fi network.
   """
   if not os.path.exists(path):
      console.print(f"[bold red][Error][/bold red] Path '{path}' does not exist.")
      raise typer.Exit(code=1)

   ip = get_local_ip()

   if ip is None:
      console.print(f"[bold red][Error][/bold red] No Network IP found. Make sure you're connected to the same network with the receiver.")
      raise typer.Exit(code=1)

   console.print(f"[yellow]Port:[/yellow] {port}")
   console.print(f"[yellow]Target Folder:[/yellow] {os.path.abspath(path)}")

   confirm_to_share_secrets_in_cwd(path)

   console.print(f"\n[bold green]Local Sharing Server started at http://{ip}:{port}[/bold green]")

   start_server(ip, port)

# ONLINE SHARE

@cli.command(name="remote")
def remote_share(
   path: str = typer.Argument(os.getcwd(), help="The directory path or file to share"),
   port: int = typer.Option(3301, "--port", "-p", help="Internal port for the tunnel"),
):
   import threading

   """
   Share files over the public internet with a remote receiver.
   """
   if not os.path.exists(path):
      console.print(f"[bold red][Error][/bold red] Path '{path}' does not exist.")
      raise typer.Exit(code=1)

   console.print(f"[bold cyan]Initializing Secure Remote Connection...[/bold cyan]")
   console.print(f"[yellow]Target Folder:[/yellow] {os.path.abspath(path)}")

   confirm_to_share_secrets_in_cwd(path)

   host = "127.0.0.1"
   t = threading.Thread(target=start_server, args=(host, port), daemon=True)
   t.start()

   console.print(f"[bold cyan]Server started, creating remote tunnel...[/bold cyan]")

   def on_url(url):
      console.print(f"\n[bold green]Remote Tunnel created at {url}[/bold green]")

   start_tunnel(port, on_url=on_url)   # blocks here, keeps process alive


if __name__ == "__main__":
   cli()
   