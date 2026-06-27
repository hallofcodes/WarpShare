from flask import Blueprint, request, send_file
from utils.safe_path import get_safe_path
import os

bp = Blueprint('download_commands', __name__)

@bp.route('/download', methods=['GET'])
def command():
   try:
      target_path = get_safe_path(request.args.get('path'))

      if not os.path.isfile(target_path):
         return "Requested path is not a file", 400

      return send_file(target_path, as_attachment=True)

   except Exception as e:
      return f"Error downloading file: {e}", 500
