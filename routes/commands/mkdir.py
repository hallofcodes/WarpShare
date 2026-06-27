from flask import Blueprint, request, jsonify
from utils.safe_path import get_safe_path
import os

bp = Blueprint('mkdir_commands', __name__)

@bp.route('/mkdir', methods=['POST'])
def command():
   try:
      data = request.get_json(silent=True) or {}
      target_path = get_safe_path(data.get('path'))
      os.makedirs(target_path, exist_ok=False)
      return jsonify({"ok": True, "path": target_path})

   except Exception as e:
      return f"Error creating folder: {e}", 500
