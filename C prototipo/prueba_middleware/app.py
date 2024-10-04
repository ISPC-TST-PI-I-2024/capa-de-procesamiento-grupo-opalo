from flask import Flask, request, jsonify
import requests
from cliente import cliente_bp
from dispositivos import dispositivos_bp
from lecturas import lecturas_bp

app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(cliente_bp, url_prefix='/clientes')
app.register_blueprint(dispositivos_bp, url_prefix='/dispositivos')
app.register_blueprint(lecturas_bp, url_prefix='/lecturas')

# Ruta de inicio
@app.route('/')
def index():
    return "Bienvenido"

#-------------------- Middleware -------------------#

# Ruta para recibir los datos desde los dispositivos ESP32
@app.route('/middleware', methods=['POST'])
def recibir_datos():
    data = request.json  # Recibe los datos en formato JSON

    # Validación básica de datos
    if not data or 'id_dispositivo' not in data or 'valor_glucosa' not in data:
        return jsonify({"error": "Datos incompletos"}), 400

    # Si los datos son válidos, podemos procesarlos (adaptación o transformación si es necesario)
    print(f"Datos recibidos: {data}")
    
    # Adaptación de los datos si es necesario
    datos_procesados = {
        'id_dispositivo': data['id_dispositivo'],
        'valor_glucosa': data['valor_glucosa'],
        'fecha_lectura': data.get('fecha_lectura', 'Fecha no proporcionada')  # Se usa un valor por defecto si no hay fecha
    }

    # Enviar los datos procesados a la API RESTful en la ruta de lecturas
    api_url = 'http://<url_de_la_api>/lectura/'
    response = requests.post(api_url, json=datos_procesados)

    # Para pruebas, podemos devolver los datos procesados en la respuesta
    if response.status_code == 201:
        return jsonify({"message": "Datos recibidos y procesados", "datos_procesados": datos_procesados}), 201
    else:
        return jsonify({"error": "Error al enviar los datos a la API"}), 500

#-------------------- Middleware -------------------#

# Ejecutamos en 0.0.0.0 para que este accesible externamente, y 
# debug=true permite que Flask recargue la aplicación automáticamente ante cambios en el código
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)