from flask import jsonify, request
from app import app
from app.models import IotDevice

@app.route('/add_sensor_data', methods=['POST'])
def add_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    new_device = IotDevice(temperature=temperature, humidity=humidity)
    new_device.save()

    return jsonify({'message': 'Sensor data added successfully'}), 201
