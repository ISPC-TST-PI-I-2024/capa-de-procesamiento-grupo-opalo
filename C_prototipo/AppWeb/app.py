from flask import Flask, request, jsonify, render_template
from datetime import datetime
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de conexión a la base de datos MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Contrasena09081994',
    'database': 'proyecto_ip'
}

# Ruta para recibir datos desde el ESP32 y almacenarlos en la tabla `medicion`
@app.route('/api/mediciones', methods=['POST'])
def recibir_medicion():
    data = request.get_json()
    if not data or 'timestamp' not in data or 'valor' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        # Insertar la medición en la tabla `medicion`
        query = """
        INSERT INTO medicion (fecha, glucemia, dispositivo_id) 
        VALUES (%s, %s, %s)
        """
        timestamp = datetime.fromtimestamp(data['timestamp'] / 1000)
        valor = data['valor']
        dispositivo_id = data.get('dispositivo_id', None)
        cursor.execute(query, (timestamp, valor, dispositivo_id))

        conexion.commit()
        return jsonify({'message': 'Medición recibida exitosamente'}), 201

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ruta para consultar todos los pacientes
@app.route('/api/pacientes', methods=['GET'])
def obtener_pacientes():
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM paciente")
        pacientes = cursor.fetchall()
        return jsonify(pacientes)

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ruta para consultar detalles de un paciente, incluyendo el contacto de emergencia
@app.route('/api/pacientes/<int:paciente_id>', methods=['GET'])
def obtener_detalles_paciente(paciente_id):
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        # Obtener detalles del paciente y su contacto de emergencia
        query_paciente = "SELECT * FROM paciente WHERE paciente_id = %s"
        query_contacto = "SELECT * FROM contacto_emergencia WHERE paciente_id = %s"
        
        cursor.execute(query_paciente, (paciente_id,))
        paciente = cursor.fetchone()

        cursor.execute(query_contacto, (paciente_id,))
        contacto = cursor.fetchone()

        if paciente:
            paciente['contacto'] = contacto
            return jsonify(paciente)
        else:
            return jsonify({'error': 'Paciente no encontrado'}), 404

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ruta para consultar lecturas de un paciente específico, filtradas por nombre o DNI
@app.route('/api/mediciones', methods=['GET'])
def obtener_lecturas_filtradas():
    query = request.args.get('query', '').lower()
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        # Filtrar por nombre o DNI del paciente y obtener las lecturas
        consulta = """
        SELECT m.medicion_id, m.fecha, m.glucemia, d.modelo AS dispositivo_modelo, p.nombre, p.apellido
        FROM medicion m
        JOIN dispositivo d ON m.dispositivo_id = d.dispositivo_id
        JOIN paciente p ON d.paciente_id = p.paciente_id
        WHERE LOWER(p.nombre) LIKE %s OR CAST(p.paciente_id AS CHAR) LIKE %s
        ORDER BY m.fecha DESC
        """
        cursor.execute(consulta, (f'%{query}%', f'%{query}%'))
        lecturas = cursor.fetchall()
        return jsonify(lecturas)

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Ruta principal de la página web de inicio
@app.route('/')
def index():
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        # Cargar todos los pacientes para mostrarlos en la lista
        cursor.execute("SELECT paciente_id, nombre, apellido FROM paciente")
        pacientes = cursor.fetchall()

        return render_template('index.html', pacientes=pacientes)

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return "Error al conectar con la base de datos", 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
