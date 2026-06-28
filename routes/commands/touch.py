from flask import Blueprint, request, jsonify
from utils.safe_path import get_safe_path
import os

bp = Blueprint('touch_commands', __name__)

@bp.route('/touch', methods=['POST'])
def command():
   try:
      data = request.get_json(silent=True) or {}
      target_path = get_safe_path(data.get('path'))
      content = data.get('content', '')

      if os.path.exists(target_path):
         return "Error creating file: File already exists", 409
      if target_path.endswith(os.sep):
         return "Error creating file: Invalid file name", 400

      parent_dir = os.path.dirname(target_path)
      if not os.path.isdir(parent_dir):
         return "Error creating file: Parent folder does not exist", 400

      with open(target_path, 'x', encoding='utf-8') as new_file:
         new_file.write(content)

      return jsonify({"ok": True, "path": target_path})

   except Exception as e:
      return f"Error creating file: {e}", 500
