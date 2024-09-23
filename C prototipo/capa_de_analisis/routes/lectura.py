from flask import Blueprint, request, jsonify
from db_config import get_db_connection

# Creamos el Blueprint para las lecturas de glucosa
lectura_bp = Blueprint('lectura', __name__)

# Endpoint para obtener todas las lecturas
@lectura_bp.route('/', methods=['GET'])
def get_lecturas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Lecturas")
    lecturas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(lecturas)

# Endpoint para obtener una lectura por su ID (id_lectura)
@lectura_bp.route('/<int:id>', methods=['GET'])
def get_lectura(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Lecturas WHERE id_lectura = %s", (id,))
    lectura = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(lectura)

# Endpoint para agregar una nueva lectura
@lectura_bp.route('/', methods=['POST'])
def add_lectura():
    nueva_lectura = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Lecturas (id_dispositivo, valor_glucosa, fecha_lectura) VALUES (%s, %s, %s)",
        (nueva_lectura['id_dispositivo'], nueva_lectura['valor_glucosa'], nueva_lectura['fecha_lectura'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 201

# Endpoint para actualizar una lectura existente
@lectura_bp.route('/<int:id>', methods=['PUT'])
def update_lectura(id):
    lectura_actualizada = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Lecturas SET id_dispositivo = %s, valor_glucosa = %s, fecha_lectura = %s WHERE id_lectura = %s",
        (lectura_actualizada['id_dispositivo'], lectura_actualizada['valor_glucosa'], lectura_actualizada['fecha_lectura'], id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

# Endpoint para eliminar una lectura
@lectura_bp.route('/<int:id>', methods=['DELETE'])
def delete_lectura(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Lecturas WHERE id_lectura = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204
