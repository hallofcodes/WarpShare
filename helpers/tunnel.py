import os, sys, stat, subprocess, urllib.request, threading, platform
from rich.console import Console

console = Console()

INSTALL_DIR = os.path.expanduser("~/.warpshare/bin")
BINARY = os.path.join(INSTALL_DIR, "cloudflared")

# Map operating systems and CPU architectures to specific download URLs
DOWNLOAD_URLS = {
   "linux": {
      "x86_64":  "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64",
      "aarch64": "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64",
      "arm64":   "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64"
   },
   "darwin": {
      "x86_64":  "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz",
      "arm64":   "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz" # universal binary
   },
   "win32": {
      "x86_64":  "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe",
      "arm64":   "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-arm64.exe"
   }
}


def download_with_progress(url, dest):
   def reporthook(block, block_size, total_size):
      if total_size == -1:
         print(f"\rDownloading {block * block_size / 1024 / 1024:.1f} MB", end="")
      else:
         downloaded = block * block_size
         percent = min(downloaded / total_size * 100, 100)
         mb_done = downloaded / 1024 / 1024
         mb_total = total_size / 1024 / 1024
         print(f"\rDownloading {percent:.1f}% ({mb_done:.1f}/{mb_total:.1f} MB)", end="")

   urllib.request.urlretrieve(url, dest, reporthook=reporthook)
   # done


def get_binary_path():
   if sys.platform == "win32":
      return BINARY + ".exe"

   return BINARY

def is_installed():
   return os.path.isfile(get_binary_path())

def install():
   sys_platform = sys.platform
   arch = platform.machine().lower() # Detects x86_64, aarch64, arm64, etc.

   # Fallback defaults to x86_64 if architecture dictionary parsing fails
   platform_urls = DOWNLOAD_URLS.get(sys_platform)
   if platform_urls is None:
      raise OSError(f"Unsupported platform: {sys_platform}")

   url = platform_urls.get(arch, platform_urls.get("x86_64"))

   os.makedirs(INSTALL_DIR, exist_ok=True)
   dest = get_binary_path()

   # If a faulty zero-byte or broken architecture binary exists, clear it first
   if os.path.exists(dest):
      os.remove(dest)

   console.print(f"[bold cyan]Downloading cloudflared for {arch} [One time download], please wait...[/bold cyan]")
   download_with_progress(url, dest)

   # Make executable on unix
   if sys_platform != "win32":
      st = os.stat(dest)
      os.chmod(dest, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

   console.print(f"\r[bold green]Installed.[/bold green] Location: {dest}")

def ensure_installed():
   if not is_installed():
      install()



def start_tunnel(port: int, on_url = None):
   import time, pexpect

   ensure_installed()

   binary = get_binary_path()
   cmd = f"{binary} tunnel --url http://127.0.0.1:{port}"

   # 30 seconds timeout for slower network connections
   child = pexpect.spawn(cmd, timeout=30)

   # Shows logs streaming in the terminal
   # child.logfile = sys.stdout.buffer

   try:
      # Expect the unique block pattern containing the URL
      child.expect(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")

      # Extract the matched text
      tunnel_url = child.match.group(0).decode("utf-8")

      if on_url:
         on_url(tunnel_url)

      # Keep the script in the foreground without printing logs
      while child.isalive():
         time.sleep(1) # Block the main thread efficiently

   except pexpect.TIMEOUT:
      console.print("\n[bold red][Error]:[/bold red] Tunnel initialization timed out!")
   except pexpect.EOF:
      console.print("\n[bold red][Error]:[/bold red] Tunnel process exited unexpectedly.")
   except KeyboardInterrupt:
      print("\nStopping remote tunnel...")
      child.terminate(force=True)
