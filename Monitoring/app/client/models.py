# app/client/models.py

from app import db

class EndDevice(db.Document):
    name = db.StringField(max_length=255, required=True)
    ip_address = db.StringField(max_length=15, required=True)
    mac_address = db.StringField(max_length=17, required=True)
    longitude = db.FloatField(required=True)
    latitude = db.FloatField(required=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"
