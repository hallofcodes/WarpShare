import os
import importlib
from flask import Flask
from routes.views import views_bp

def create_app():
   app = Flask(__name__)

   app.register_blueprint(views_bp)

   # AUTOMATICALLY REGISTER ALL FILES IN COMMANDS DIR
   commands_dir = os.path.join(os.path.dirname(__file__), 'routes', 'commands')

   for filename in os.listdir(commands_dir):
      if filename.endswith('.py') and filename != '__init__.py':
         module_name = filename[:-3]  # Strip '.py' extension

         module = importlib.import_module(f'routes.commands.{module_name}')

         if hasattr(module, 'bp'):
            app.register_blueprint(module.bp, url_prefix="/commands")

         elif hasattr(module, f"{module_name}_bp"):
            bp_object = getattr(module, f"{module_name}_bp")
            app.register_blueprint(bp_object, url_prefix="/commands")

   return app

