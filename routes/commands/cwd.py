from flask import Blueprint
import stores.user_current_shared_path as shared_path

bp = Blueprint('cwd_commands', __name__)

@bp.route('/cwd', methods=['GET'])
def command():
   return shared_path.path
