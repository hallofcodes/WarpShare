from flask import Blueprint, render_template

# Create the blueprint
views_bp = Blueprint('views', __name__)

@views_bp.route('/')
def home():
   return render_template('index.html', title="Home Page")
