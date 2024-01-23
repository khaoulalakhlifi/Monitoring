# app/client/routes.py

from flask import render_template, Blueprint, request, redirect, url_for
from app.client.models import EndDevice  # Assurez-vous d'importer le modèle approprié

client_bp = Blueprint('client', __name__)

@client_bp.route('/client/dashboard')
def client_dashboard():
    # Logique pour récupérer les données nécessaires à partir de la base de données ou d'autres sources
    # Par exemple, vous pouvez récupérer une liste d'appareils IoT
    iot_devices = EndDevice.objects()  # Utilisez la logique appropriée pour récupérer les appareils IoT depuis la base de données

    # Rendre le template en passant les données récupérées
    return render_template('client/dashboard.html', iot_devices=iot_devices)

@client_bp.route('/client/add_device', methods=['GET', 'POST'])
def add_device():
    if request.method == 'POST':
        # Logique pour traiter les données du formulaire
        name = request.form.get('name')
        ip_address = request.form.get('ip_address')
        mac_address = request.form.get('mac_address')
        longitude = float(request.form.get('longitude'))
        latitude = float(request.form.get('latitude'))

        # Création d'une nouvelle instance EndDevice avec les données du formulaire
        new_device = EndDevice(name=name, ip_address=ip_address, mac_address=mac_address, longitude=longitude, latitude=latitude)
        
        # Enregistrement de l'instance dans la base de données
        new_device.save()

        # Redirection vers le tableau de bord après l'ajout du périphérique
        return redirect(url_for('client.client_dashboard'))

    # Si la méthode est GET, simplement rendre le formulaire
    return render_template('client/add_device.html')
