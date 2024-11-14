[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/orSi9ChT)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=15972966&assignment_repo_type=AssignmentRepo)


![Caratula](/E%20Recursos/caratulaPI.png)
## Instituto: ISPC  
**Carrera:** [Tecnicatura Superior en Telecomunicaciones](https://www.ispc.edu.ar/tecnicatura-superior-en-telecomunicaciones/)  
**Materia:** Proyecto Integrador I  
**Docente:** Cristian Gonzalo Vera

## Grupo: OPALO <img src="https://stardewvalleywiki.com/mediawiki/images/3/3c/Opal.png"  width="10%" height="100%">
**Integrantes:**
- Vittorio Durgutti ([GitHub](https://github.com/vittoriodurigutti))
- Luciano Lujan ([GitHub](https://github.com/lucianoilujan))
- Dario Arriola ([GitHub](https://github.com/dr-arriola))
- Jose Marquez ([GitHub](https://github.com/marquezjose))
- Joaquin Garzon ([GitHub](https://github.com/Joacogarzonn))
- Lisandro Juncos ([GitHub](https://github.com/Lisandro-05))
- Nahuel Velez ([GitHub](https://github.com/Lucasmurua19))
- Marcos Bordon Rios ([GitHub](https://github.com/Marcos-BR-03))
- Tiziano Paez ([GitHub](https://github.com/tpaez))

---

## Capa de Procesamiento 

### Sistema IoT para un dispositivo Medidor de Glucosa

### Descripción del Proyecto:
El proyecto consiste en el desarrollo de un medidor de glucosa IoT que utiliza un microcontrolador ESP32, un sensor óptico CNY 70 y un panel táctil para el encendido y control del dispositivo. Este medidor será capaz de capturar y procesar los niveles de glucosa en sangre, y enviar la información a una plataforma en la nube para su almacenamiento y análisis. El objetivo es proporcionar un dispositivo compacto, fácil de usar y conectado, que permita a los usuarios monitorear sus niveles de glucosa en tiempo real y acceder a sus datos desde cualquier lugar.

---

### Etapa Actual: Capa de Procesamiento
En esta etapa del proyecto, estamos centrados en el procesamiento de datos, implementando la capa de backend que gestionará la interacción entre el dispositivo IoT y la plataforma en la nube. Estamos trabajando en el desarrollo de una API RESTful para la comunicación con la base de datos y la gestión de datos críticos del sistema IoT, como dispositivos, usuarios, proyectos y sus configuraciones.

---

### Estructura del repositorio:
- A requisitos
- B investigacion
- C prototipo
    - capa_de_analisis:
        - app.py: Archivo principal de la aplicación, donde se inicializa Flask y se registran las rutas API.
        - db_config.py: Contiene la configuración de la base de datos MySQL, incluyendo las conexiones y parámetros de acceso.
        - models.py: Define los modelos de datos (tablas) para el sistema usando SQLAlchemy.
        - routes: Carpeta que contiene todos los Blueprints que manejan las diferentes rutas de la API.
            - lectura.py: Maneja las lecturas captadas por cada dispositivo.
            - dispositivos.py: Gestión de dispositivos registrados en el sistema.
            - seguridad.py: Implementa mecanismos de autenticación y autorización.
            - cliente.py: Gestiona la información de los usuarios registrados en el sistema.
        - requirements.txt: Lista de todas las dependencias del proyecto (incluyendo Flask y SQLAlchemy).
        - Dockerfile: Archivo que contiene las instrucciones para construir y desplegar la aplicación en un entorno Docker.
- D presentacion
- E recursos

---

### Stack Tecnológico
El stack tecnológico utilizado en este proyecto incluye:
- Lenguaje de programación: Python
- Framework web: Flask
- Base de datos: MySQL
- ORM: SQLAlchemy
- Plataforma de despliegue: Docker
- Microcontrolador: ESP32 (para la conexión IoT)
- Sensor: CNY 70 (para la captura de datos de glucosa)
- Panel táctil: Para la interacción del usuario con el dispositivo (opcional)
- Plataforma en la nube: Conexion a un servidor brindado por el profesor. 
     - **comando:** ssh opalo@gonaiot.com **password** opalo

---

### Licencia

MIT License

Copyright (c) [2024] [Sistema IoT para un dispositivo Medidor de Glucosa/Integrates Equipo Opao]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
