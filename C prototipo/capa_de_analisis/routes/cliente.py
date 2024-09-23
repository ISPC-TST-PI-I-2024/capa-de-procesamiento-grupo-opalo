from flask import Blueprint, request, jsonify
from db_config import get_db_connection

# Creamos el Blueprint para los clientes
cliente_bp = Blueprint('clientes', __name__)

# Endpoint para obtener todos los clientes
@cliente_bp.route('/', methods=['GET'])
def get_clientes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cliente")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(clientes)

# Endpoint para obtener un cliente específico por su dni
@cliente_bp.route('/<int:dni>', methods=['GET'])
def get_cliente(dni):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Cliente WHERE dni = %s", (dni,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(cliente)

# Endpoint para agregar un nuevo cliente
@cliente_bp.route('/', methods=['POST'])
def add_cliente():
    nuevo_cliente = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO Cliente (dni, nombre, apellido, fecha_nacimiento, telefono_1, telefono_2, email, provincia, localidad, calle, altura, depto, observacion)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (
            nuevo_cliente['dni'], nuevo_cliente['nombre'], nuevo_cliente['apellido'], 
            nuevo_cliente['fecha_nacimiento'], nuevo_cliente['telefono_1'], 
            nuevo_cliente.get('telefono_2'), nuevo_cliente['email'], 
            nuevo_cliente['provincia'], nuevo_cliente['localidad'], 
            nuevo_cliente['calle'], nuevo_cliente['altura'], 
            nuevo_cliente.get('depto'), nuevo_cliente.get('observacion')
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 201

# Endpoint para actualizar un cliente existente
@cliente_bp.route('/<int:dni>', methods=['PUT'])
def update_cliente(dni):
    cliente_actualizado = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Cliente 
           SET nombre = %s, apellido = %s, fecha_nacimiento = %s, telefono_1 = %s, telefono_2 = %s, 
               email = %s, provincia = %s, localidad = %s, calle = %s, altura = %s, 
               depto = %s, observacion = %s
           WHERE dni = %s""",
        (
            cliente_actualizado['nombre'], cliente_actualizado['apellido'], 
            cliente_actualizado['fecha_nacimiento'], cliente_actualizado['telefono_1'], 
            cliente_actualizado.get('telefono_2'), cliente_actualizado['email'], 
            cliente_actualizado['provincia'], cliente_actualizado['localidad'], 
            cliente_actualizado['calle'], cliente_actualizado['altura'], 
            cliente_actualizado.get('depto'), cliente_actualizado.get('observacion'), dni
        )
    )
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204

# Endpoint para eliminar un cliente
@cliente_bp.route('/<int:dni>', methods=['DELETE'])
def delete_cliente(dni):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Cliente WHERE dni = %s", (dni,))
    conn.commit()
    cursor.close()
    conn.close()
    return '', 204
