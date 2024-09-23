from flask import Flask
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

# Ejecutamos en 0.0.0.0 para que este accesible externamente, y 
# debug=true permite que Flask recargue la aplicación automáticamente ante cambios en el código
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
