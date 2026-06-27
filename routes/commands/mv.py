from flask import Blueprint, request
from utils.safe_path import get_safe_path
import stores.user_current_shared_path as shared_path
import shutil
import os

bp = Blueprint('mv_commands', __name__)

@bp.route('/mv', methods=['POST'])
def command():
   try:
      data = request.get_json()

      from_path = get_safe_path(data.get('from_path'))
      dest_path = get_safe_path(data.get('dest_path'))
   
      return shutil.move(from_path, dest_path)

   except Exception as e:
      return f"Error moving file/folder: {e}", 500
