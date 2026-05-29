import fnmatch
import click, sys
from rich.console import Console
from pathlib import Path

console = Console()

EXACT_SECRETS = (
   ".env",
   ".nprc",
   ".yarnrc",
   ".pypirc",
   ".netrc",
   ".git-credentials",
   "id_rsa",
   "id_ed25519",
   "authorized_keys",
   "secrets.yaml",
   "terraform.tfvars",
   "wp-config.php",
   "database.yml",
   "service-account.json",
   "gcloud.json",
   "azureProfile.json",
)

WILDCARD_SECRETS = (
   "*.pem",
   "*.key",
   "*.p12",
   "*.pfx",
   "*.crt",
   "*.cer",
   "*.keystore",
   ".env.*",
)


def confirm_to_share_secrets_in_cwd(path: str) -> None:
   path = Path(path)
   is_asked = False

   # 2. Iterate through files in the directory
   for file_path in path.iterdir():
      if file_path.is_file():
         name = file_path.name
      else:
         continue

      # Check exact match
      if name in EXACT_SECRETS:
         ask(name, is_asked)
         is_asked = True

      # Check wildcard match
      if any(fnmatch.fnmatch(name, pattern) for pattern in WILDCARD_SECRETS):
         ask(name, is_asked)
         is_asked = True


def ask(filename: str, is_asked: bool) -> None:
   if not is_asked:
      console.print(f"\n[bold yellow][Warning][/bold yellow] This file may contain secrets, credentials, or private keys.")
   else:
      print()

   console.print(f"[bold red][File][/bold red] {filename}")
   console.print("\nAre you sure to share it with the receiver? (y/N)", end=" ")
   value: str = click.getchar().lower()

   print()

   if value != "y":
      sys.exit()
   return
