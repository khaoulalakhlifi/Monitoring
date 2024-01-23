# app/admin/models.py

from app import db
from datetime import datetime

class AdminUser(db.Document):
    username = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    email = db.EmailField()
    full_name = db.StringField()
    role = db.StringField(default='admin')  # Rôle par défaut pour les utilisateurs admin
    created_at = db.DateTimeField(default=datetime.utcnow)  # Date de création automatique

    # Ajoutez d'autres champs en fonction des besoins
    phone_number = db.StringField()
    department = db.StringField()

    def __repr__(self):
        return f"AdminUser(username={self.username}, email={self.email}, full_name={self.full_name}, role={self.role}, created_at={self.created_at}, phone_number={self.phone_number}, department={self.department})"
