# Fichier app/models.py
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Document):
    id = db.IntField(primary_key=True)
    username = db.StringField(max_length=50, unique=True, required=True)
    password_hash = db.StringField(max_length=128, required=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Client(db.Document):
    client_type = db.StringField(max_length=50, required=True)
    name = db.StringField(max_length=100, required=True)
    # Ajoutez d'autres champs communs ici

    # Champs spécifiques à chaque type de client
    ip_address = db.StringField(max_length=15)
    mac_address = db.StringField(max_length=17)
    mqtt_topic = db.StringField(max_length=100)
    longitude = db.FloatField()
    latitude = db.FloatField()
    # Ajoutez d'autres champs spécifiques ici en fonction des besoins

    def __repr__(self):
        return f"Client(client_type={self.client_type}, name={self.name}, ...)"
