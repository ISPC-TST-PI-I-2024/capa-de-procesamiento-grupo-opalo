import mysql.connector
from mysql.connector import Error

# definimo la conexion al servidor, segun el asignado (opalo@gonaiot.com Pass: opalo)
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='gonaiot.com',    
            database='Capa_Procesamiento',
            user='opalo',          
            password='opalo' 
        )
        
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

