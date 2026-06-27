from flask import Blueprint, request, jsonify
from utils.safe_path import get_safe_path
import os
import shutil

bp = Blueprint('rm_commands', __name__)

@bp.route('/rm', methods=['POST', 'DELETE'])
def command():
   try:
      data = request.get_json(silent=True) or {}
      target_path = get_safe_path(data.get('path') or request.args.get('path'))

      if os.path.isdir(target_path):
         shutil.rmtree(target_path)
      else:
         os.remove(target_path)

      return jsonify({"ok": True})

   except Exception as e:
      return f"Error deleting file/folder: {e}", 500
