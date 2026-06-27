from flask import Blueprint, render_template
import stores.share_status as share_status

# Create the blueprint
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
   return render_template(
      'index.html',
      status=share_status.status,
      title="WarpShare",
      display_name="WarpShare"
   )
