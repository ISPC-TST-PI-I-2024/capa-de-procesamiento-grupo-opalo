from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
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

# ------------------------------
# Bloque para registrar datos del ESP32
# ------------------------------

@app.route('/api/mediciones', methods=['POST'])
def recibir_medicion():
    """Recibe los datos de medición de glucemia desde el ESP32 y los guarda en la base de datos."""
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

# ------------------------------
# Bloques para obtener información de la base de datos
# ------------------------------

@app.route('/api/pacientes', methods=['GET'])
def obtener_pacientes():
    """Obtiene todos los pacientes de la base de datos."""
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

@app.route('/api/mediciones', methods=['GET'])
def obtener_lecturas_filtradas():
    """Obtiene las lecturas de glucemia filtradas por nombre o DNI del paciente."""
    query = request.args.get('query', '').lower()
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

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

@app.route('/api/mediciones/ultimas', methods=['GET'])
def obtener_ultimas_mediciones():
    """Obtiene las últimas mediciones según un rango de tiempo especificado (en horas, días, semanas)."""
    rango = request.args.get('rango', '24h')  # Ejemplo de formato: '24h', '7d', '1w'
    intervalo = None
    if 'h' in rango:
        intervalo = datetime.now() - timedelta(hours=int(rango.replace('h', '')))
    elif 'd' in rango:
        intervalo = datetime.now() - timedelta(days=int(rango.replace('d', '')))
    elif 'w' in rango:
        intervalo = datetime.now() - timedelta(weeks=int(rango.replace('w', '')))

    if not intervalo:
        return jsonify({'error': 'Rango de tiempo inválido'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        consulta = """
        SELECT m.medicion_id, m.fecha, m.glucemia, d.modelo AS dispositivo_modelo, p.nombre, p.apellido
        FROM medicion m
        JOIN dispositivo d ON m.dispositivo_id = d.dispositivo_id
        JOIN paciente p ON d.paciente_id = p.paciente_id
        WHERE m.fecha >= %s
        ORDER BY m.fecha DESC
        """
        cursor.execute(consulta, (intervalo,))
        lecturas = cursor.fetchall()
        return jsonify(lecturas)

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/api/dispositivos', methods=['GET'])
def obtener_dispositivos_y_clientes():
    """Obtiene todos los dispositivos junto con los datos de los clientes asociados."""
    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        consulta = """
        SELECT d.dispositivo_id, d.modelo, d.fecha_fabricacion, d.fecha_colocacion, d.fabricante,
               p.paciente_id, p.nombre AS paciente_nombre, p.apellido AS paciente_apellido
        FROM dispositivo d
        LEFT JOIN paciente p ON d.paciente_id = p.paciente_id
        """
        cursor.execute(consulta)
        dispositivos = cursor.fetchall()
        return jsonify(dispositivos)

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# ------------------------------
# Bloques para insertar datos en la base de datos
# ------------------------------

@app.route('/api/pacientes', methods=['POST'])
def agregar_paciente():
    """Agrega un nuevo paciente a la base de datos."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        query = """
        INSERT INTO paciente (nombre, apellido, fecha_nacimiento, sexo, direccion, peso, altura, correo, telefono)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['nombre'], data['apellido'], data['fecha_nacimiento'], data['sexo'], 
            data['direccion'], data['peso'], data['altura'], data['correo'], data['telefono']
        ))

        conexion.commit()
        return jsonify({'message': 'Paciente agregado exitosamente'}), 201

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/api/dispositivos', methods=['POST'])
def agregar_dispositivo_a_cliente():
    """Asocia un nuevo dispositivo a un paciente específico."""
    data = request.get_json()
    if not data or 'paciente_id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        query = """
        INSERT INTO dispositivo (modelo, fecha_fabricacion, fecha_colocacion, fabricante, paciente_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            data['modelo'], data['fecha_fabricacion'], data['fecha_colocacion'], 
            data['fabricante'], data['paciente_id']
        ))

        conexion.commit()
        return jsonify({'message': 'Dispositivo agregado exitosamente'}), 201

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# ------------------------------
# Bloques para modificar datos en la base de datos
# ------------------------------

@app.route('/api/pacientes/<int:paciente_id>', methods=['PUT'])
def modificar_paciente(paciente_id):
    """Modifica los datos de un paciente específico."""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        query = """
        UPDATE paciente
        SET nombre = %s, apellido = %s, fecha_nacimiento = %s, sexo = %s, direccion = %s,
            peso = %s, altura = %s, correo = %s, telefono = %s
        WHERE paciente_id = %s
        """
        cursor.execute(query, (
            data['nombre'], data['apellido'], data['fecha_nacimiento'], data['sexo'], 
            data['direccion'], data['peso'], data['altura'], data['correo'], data['telefono'], paciente_id
        ))

        conexion.commit()
        return jsonify({'message': 'Paciente modificado exitosamente'}), 200

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

@app.route('/api/dispositivos/<int:dispositivo_id>', methods=['PUT'])
def cambiar_dispositivo_cliente(dispositivo_id):
    """Cambia el dispositivo de un cliente específico."""
    data = request.get_json()
    if not data or 'paciente_id' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    try:
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        query = """
        UPDATE dispositivo
        SET paciente_id = %s
        WHERE dispositivo_id = %s
        """
        cursor.execute(query, (data['paciente_id'], dispositivo_id))

        conexion.commit()
        return jsonify({'message': 'Dispositivo cambiado exitosamente'}), 200

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()

# ------------------------------
# Bloques para eliminar datos de la base de datos
# ------------------------------

# Bloque para eliminar datos de la base de datos
@app.route('/api/pacientes/<int:paciente_id>', methods=['DELETE'])
def eliminar_paciente(paciente_id):
    """Elimina un paciente y todos sus datos asociados después de una confirmación."""

    # Verificar el parámetro de confirmación en la solicitud
    confirm = request.args.get('confirm', 'no').lower()
    if confirm != 'yes':
        # Si no se envía confirmación, solicitamos confirmación
        return jsonify({'message': '¿Está seguro que desea eliminar este elemento del registro? Añada `?confirm=yes` para confirmar.'}), 400

    try:
        # Conectar a la base de datos
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        # Eliminar el paciente (y sus datos asociados en cascada)
        query = "DELETE FROM paciente WHERE paciente_id = %s"
        cursor.execute(query, (paciente_id,))

        conexion.commit()
        return jsonify({'message': 'Paciente y datos asociados eliminados exitosamente'}), 200

    except Error as e:
        print(f"Error al conectar con MySQL: {e}")
        return jsonify({'error': 'Error al conectar con la base de datos'}), 500

    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()


# Iniciar el servidor
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
