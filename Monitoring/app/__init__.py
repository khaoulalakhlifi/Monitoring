# app/__init__.py

from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialisation de MongoEngine avec l'application Flask
db = MongoEngine(app)

# Importez vos routes
from app.admin.routes import admin_bp
from app.client.routes import client_bp

# Enregistrez les blueprints
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(client_bp, url_prefix='/client')
