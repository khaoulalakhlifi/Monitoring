from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



@app.route('/')
def index():
    clients = Client.query.all()
    return render_template('client_list.html', clients=clients)

# Modifiez votre modèle Client dans app.py
class Client(db.Document):
    # Fields of the Client model
    client_type = db.StringField(max_length=50, required=True)
    name = db.StringField(max_length=100, required=True)
    ip_address = db.StringField(max_length=15)
    mac_address = db.StringField(max_length=17)
    mqtt_topic = db.StringField(max_length=100)
    longitude = db.FloatField()
    latitude = db.FloatField()
    temperature = db.FloatField()  # Ajoutez ce champ


@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        client_type = request.form.get('client_type')
        name = request.form.get('name')
        ip_address = request.form.get('ip_address')
        mac_address = request.form.get('mac_address')
        mqtt_topic = request.form.get('mqtt_topic')
        longitude = request.form.get('longitude')
        latitude = request.form.get('latitude')

        new_client = Client(
            client_type=client_type,
            name=name,
            ip_address=ip_address,
            mac_address=mac_address,
            mqtt_topic=mqtt_topic,
            longitude=longitude,
            latitude=latitude
        )
        db.session.add(new_client)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('add_client.html')



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
