from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database_name',
    'host': 'your_mongodb_uri',
}
db = MongoEngine(app)

from app import routes
