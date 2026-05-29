from flask import Flask
from routes.views import views_bp
# from routes.fs import fs_bp
# from routes.uploads import uploads_bp

def create_app():
   app = Flask(__name__)

   app.register_blueprint(views_bp)
   # app.register_blueprint(fs_bp, url_prefix="/api")
   # app.register_blueprint(uploads_bp, url_prefix="/api")

   return app

