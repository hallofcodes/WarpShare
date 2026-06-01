from flask import Blueprint

bp = Blueprint('cwd_commands', __name__)

@bp.route('/cwd', methods=['GET'])
def command():
   return shared_path.path
