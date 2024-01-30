# prediction_module.py
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd

def train_model(data):
    # Séparez les variables d'entrée (X) et les variables cibles (y)
    X = data[['temperature_2m', 'relative_humidity_2m']]
    y_temperature = data['temperature_2m']
    y_humidity = data['relative_humidity_2m']

    # Divisez les données en ensembles d'entraînement et de test
    X_train, X_test, y_temp_train, y_temp_test, y_hum_train, y_hum_test = train_test_split(
        X, y_temperature, y_humidity, test_size=0.2, random_state=42)

    # Initialisez le modèle de régression linéaire
    model_temperature = LinearRegression()
    model_humidity = LinearRegression()

    # Entraînez les modèles
    model_temperature.fit(X_train, y_temp_train)
    model_humidity.fit(X_train, y_hum_train)

    # Prédisez sur l'ensemble de test
    y_temp_pred = model_temperature.predict(X_test)
    y_hum_pred = model_humidity.predict(X_test)

    # Évaluez la performance des modèles
    mse_temp = mean_squared_error(y_temp_test, y_temp_pred)
    mse_hum = mean_squared_error(y_hum_test, y_hum_pred)

    print(f'Mean Squared Error for Temperature: {mse_temp}')
    print(f'Mean Squared Error for Humidity: {mse_hum}')

    return model_temperature, model_humidity

def make_prediction(models, new_data):
    # Préparez les nouvelles données pour la prédiction
    X_new = pd.DataFrame([new_data])

    # Faites la prédiction
    prediction_temperature = models[0].predict(X_new)
    prediction_humidity = models[1].predict(X_new)

    return prediction_temperature[0], prediction_humidity[0]
