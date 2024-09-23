from flask import Blueprint, request, jsonify
from db_config import get_db_connection

# Creamos el Blueprint para los dispositivos
dispositivos_bp = Blueprint('dispositivos', __name__)

# Endpoint para obtener todos los dispositivos
@dispositivos_bp.route('/', methods=['GET'])
def get_dispositivos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Dispositivos")
    dispositivos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(dispositivos)

# Endpoint para obtener un dispositivo específico por su id_dispositivo (MAC)
@dispositivos_bp.route('/<string:id_dispositivo>', methods=['GET'])
def get_dispositivo(id_dispositivo):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Dispositivos WHERE id_dispositivo = %s", (id_dispositivo,))
    dispositivo = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(dispositivo)

# Endpoint para agregar un nuevo dispositivo
@dispositivos_bp.route('/', methods=['POST'])
def add_dispositivo():
    nuevo_dispositivo = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Dispositivos (id_dispositivo, dni_cliente, fecha_colocacion, fecha_retiro) VALUES (%s, %s, %s, %s)",
        (nuevo_dispositivo['id_dispositivo'], nuevo_dispositivo['dni_cliente'], nuevo_dispositivo['fecha_colocacion'], nuevo_dispositivo.get('fecha_retiro'))
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 201

# Endpoint para actualizar un dispositivo existente
@dispositivos_bp.route('/<string:id_dispositivo>', methods=['PUT'])
def update_dispositivo(id_dispositivo):
    dispositivo_actualizado = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Dispositivos SET dni_cliente = %s, fecha_colocacion = %s, fecha_retiro = %s WHERE id_dispositivo = %s",
        (dispositivo_actualizado['dni_cliente'], dispositivo_actualizado['fecha_colocacion'], dispositivo_actualizado.get('fecha_retiro'), id_dispositivo)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

# Endpoint para eliminar un dispositivo
@dispositivos_bp.route('/<string:id_dispositivo>', methods=['DELETE'])
def delete_dispositivo(id_dispositivo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Dispositivos WHERE id_dispositivo = %s", (id_dispositivo,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204
