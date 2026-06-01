from flask import Blueprint, request
from utils.safe_path import get_safe_path
import stores.user_current_shared_path as shared_path
import shutil
import os

bp = Blueprint('cp_commands', __name__)

@bp.route('/cp', methods=['POST'])
def command():
   try:
      data = request.get_json()

      from_path = get_safe_path(data.get('from_path'))
      dest_path = get_safe_path(data.get('dest_path'))

      if os.path.isdir(from_path):
         return shutil.copytree(from_path, dest_path)
      else:
         return shutil.copy(from_path, dest_path)

   except Exception as e:
      return f"Error copying file/folder: {e}", 500
