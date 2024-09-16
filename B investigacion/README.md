[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/orSi9ChT)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=15972966&assignment_repo_type=AssignmentRepo)

![Caratula](/E%20Recursos/caratulaPI.png)


# Proyecto "Dispositivo IoT para Monitoreo Continuo de Glucosa en Pacientes Diabéticos"
  
  ## Profesor: CRISTIAN GONZALO VERA
  ## Integrantes:

- Vittorio Durgutti ([GitHub](https://github.com/vittoriodurigutti))
- Luciano Lujan ([GitHub](https://github.com/lucianoilujan))
- Rodolfo Paz (GitHub) ([GitHub](https://github.com/Domi74))
- Jose Marquez ([GitHub](https://github.com/marquezjose))
- Joaquin Garzon ([GitHub](https://github.com/Joacogarzonn))
- Lisandro Juncos ([GitHub](https://github.com/Lisandro-05))
- Nahuel Velez ([GitHub](https://github.com/Lucasmurua19))
- Marcos Bordon Rios ([GitHub](https://github.com/Marcos-BR-03))
- Tiziano Paez ([GitHub](https://github.com/tpaez))



## Proyecto IoT: Dispositivo de Monitoreo de Glucosa
-  ### Descripción General:  

Este proyecto tiene como objetivo desarrollar un dispositivo IoT para el monitoreo continuo de los niveles de glucosa en pacientes diabéticos. El enfoque de esta investigación se centra en la capa de preprocesamiento, que abarca las capas de EDGE, FOG y CLOUD. El preprocesamiento de los datos es crucial para asegurar que la información recolectada por el dispositivo sea precisa, segura y procesable en tiempo real.

* ## Estructura del Proyecto
### 1. Capa EDGE  
#### Descripción:  
La capa EDGE es la primera línea de procesamiento en el dispositivo IoT. Esta capa es responsable de la adquisición de datos y el preprocesamiento inicial antes de que la información sea transmitida a las capas superiores.

#### Especificaciones:

- Captura de Datos: Los sensores de glucosa integrados en el dispositivo capturan datos en tiempo real. Estos datos pueden incluir niveles de glucosa, temperatura del sensor, y otros parámetros fisiológicos relevantes.  

- Filtrado de Señal: Se aplican técnicas de filtrado para eliminar ruido y artefactos en los datos crudos.
Normalización de Datos: Los datos de glucosa se normalizan para asegurar consistencia en las unidades de medida.  

- Compresión de Datos: Implementación de algoritmos de compresión ligera para reducir la cantidad de datos a transmitir sin pérdida significativa de información.
Seguridad: Encriptación básica de datos antes de la transmisión para garantizar la privacidad del paciente.  

### 2. Capa FOG
#### Descripción:  
La capa FOG actúa como una extensión de la capa EDGE y permite un procesamiento intermedio antes de que los datos sean enviados a la nube. Esta capa reduce la latencia y permite una respuesta más rápida en tiempo real.

#### Especificaciones:

- Análisis Local: Los datos preprocesados en la capa EDGE son sometidos a análisis más avanzados, como la detección de patrones anómalos que podrían indicar condiciones peligrosas para el paciente (e.g., hipoglucemia o hiperglucemia). 

- Almacenamiento Temporal: Se utiliza almacenamiento local para guardar datos críticos que pueden ser retransmitidos en caso de pérdida de conexión.  

- Toma de Decisiones: Implementación de algoritmos de toma de decisiones locales, permitiendo acciones inmediatas como la activación de alertas al paciente si se detectan niveles peligrosos de glucosa.  

- Balanceo de Carga: Gestión de la carga de datos para optimizar el uso del ancho de banda disponible y mejorar la eficiencia del sistema.  

- Seguridad Avanzada: Se aplica una segunda capa de encriptación y autenticación de datos para proteger la integridad y confidencialidad de la información durante la transmisión a la nube.  

### 3. Capa CLOUD
#### Descripción:
La capa CLOUD es la última etapa en el procesamiento de datos, encargada del almacenamiento masivo, análisis a gran escala y acceso remoto a la información.  

#### Especificaciones:

- Almacenamiento en la Nube: Los datos recolectados y procesados en las capas EDGE y FOG son almacenados en la nube para análisis posteriores y acceso por parte de profesionales de la salud.  

- Análisis Predictivo: Utilización de algoritmos de aprendizaje automático para predecir tendencias en los niveles de glucosa y proporcionar recomendaciones personalizadas.  

- Dashboard de Monitoreo: Desarrollo de interfaces web y aplicaciones móviles para que los pacientes y médicos puedan visualizar los datos en tiempo real, acceder a históricos y recibir alertas.  

- Integración con Otros Sistemas: La capa CLOUD permite la integración con sistemas de gestión hospitalaria, registros médicos electrónicos (EMR), y otros dispositivos médicos IoT.  

- Seguridad y Cumplimiento: Cumplimiento con normativas de privacidad de datos como HIPAA y GDPR, asegurando la protección de la información sensible del paciente.  

### Objetivos de la Investigación
- Optimización del Preprocesamiento:  
 Investigar y desarrollar técnicas eficientes de preprocesamiento en las capas EDGE y FOG para mejorar la calidad de los datos transmitidos.  

- Reducción de Latencia:  
 Minimizar la latencia en la transmisión y procesamiento de datos a través de las diferentes capas.  
- Seguridad de Datos:  
 Implementar y evaluar métodos avanzados de encriptación y autenticación a lo largo de las tres capas para garantizar la seguridad y privacidad de los datos.  

- Escalabilidad:  
 Desarrollar una arquitectura escalable que permita la integración de múltiples dispositivos y el manejo de grandes volúmenes de datos.  
     
 ## **Conclusión**
### *La implementación de un sistema IoT para el monitoreo de glucosa basado en una arquitectura de procesamiento en capas (EDGE, FOG y CLOUD) es fundamental para asegurar un análisis eficiente y en tiempo real de los datos, garantizando al mismo tiempo la seguridad y privacidad de la información. Este enfoque no solo mejora la calidad del monitoreo de salud, sino que también permite una intervención médica más rápida y precisa.*

