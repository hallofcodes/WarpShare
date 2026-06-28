import os
from flask import abort
import stores.user_current_shared_path as shared_path

def get_safe_path(target_path: str = '.', root_path: str = None) -> str:
   """
   Resolve a user-provided path inside the shared root.
   Allows the root itself (`.`, `/`, empty) while blocking traversal outside it.
   """
   if not root_path:
      root_path = shared_path.path

   if not root_path:
      abort(400, description="Shared path is not configured.")

   if target_path is None or target_path == '':
      target_path = '.'

   abs_root = os.path.abspath(os.path.realpath(root_path))
   abs_target = os.path.abspath(os.path.realpath(os.path.join(abs_root, str(target_path).lstrip('/'))))

   try:
      if os.path.commonpath([abs_root, abs_target]) != abs_root:
         abort(403, description="Access Denied: Invalid path.")
   except ValueError:
      abort(403, description="Access Denied: Invalid path.")
   return abs_target
