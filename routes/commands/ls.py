from flask import Blueprint, request, jsonify
import stores.user_current_shared_path as shared_path
from utils.safe_path import get_safe_path
import os

bp = Blueprint('ls_commands', __name__)

@bp.route('/ls', methods=['GET'])
def command():
   try:
      target_dir = get_safe_path(request.args.get('path'))

      items = []
      for entry in os.scandir(target_dir):
          items.append({
             "name": entry.name,
             "type": "dir" if entry.is_dir() else "file",
             "size": None if entry.is_dir() else entry.stat().st_size,
             "modified": entry.stat().st_mtime
          })

      return jsonify(items)

   except Exception as e:
      return f"Error listing files/directories: {e}", 500
