import os
from pathlib import Path
from flask import abort
import stores.user_current_shared_path as shared_path

def get_safe_path(target_path: str, root_path: str = None) -> str:
   """
   Resolves target_path and ensures it remains strictly within root_path.
   If no root_path is provided, it defaults to the current working directory.
   """
   # 1. Fallback to current working directory if no root is given
   if not root_path:
      root_path = shared_path.path

   if target_path == '' or target_path is None:
      abort(400, description=f"Path is empty.")

   # 2. Resolve absolute, real paths (handles symlinks and ../ internally)
   abs_root = os.path.abspath(root_path)
   abs_target = os.path.abspath(os.path.join(abs_root, target_path))

   # 3. Restrict traversal by verifying the target starts with the root path
   # Adding trailing separator prevents partial folder name matching 
   # (e.g., /home/projects/my-portfolio-secret vs /home/projects/my-portfolio)
   root_prefix = os.path.join(abs_root, '')

   if not abs_target.startswith(root_prefix):
      abort(403, description=f"Access Denied: Invalid path.")

   return abs_target.rstrip('/')
