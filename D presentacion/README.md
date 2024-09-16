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

   

##  Descripción del Proyecto:

El proyecto consiste en el desarrollo de un dispositivo IoT avanzado diseñado para el monitoreo continuo y en tiempo real de los niveles de glucosa en pacientes diabéticos. Este dispositivo, integrado con sensores de última generación, permite medir los niveles de glucosa en la sangre de manera no invasiva o mínimamente invasiva y transmite los datos recopilados a una plataforma en la nube a través de conectividad inalámbrica.

## Componentes del Proyecto:

### 1. Recoleccion de datos (capa de percepción):
- Sensor de Glucosa: Un sensor preciso y confiable que mide los niveles de glucosa en la sangre. Puede ser un parche de detección continua o un dispositivo mínimamente invasivo que se coloca en la piel del paciente. Estos sensores estarán conectados a microcontroladores ESP32-Wroom para recolectar datos sobre los niveles de glucosa de cada paciente.
    #### Los tipos de sensores pueden ser:  

	- Sensor Optico Reflectivo Infrarrojo CNY70.  

	- Sensor NIR (técnica espectroscópica que utiliza de forma natural el espectro electromagnético).

### 2. Preprocesamiento de Datos en el Edge (Capa de Preprocesamiento):
**Módulo de Conectividad IoT:** Un módulo ESP32 Wroom que permite la conexión del sensor con una plataforma en la nube. Esto puede incluir conectividad Wi-Fi, Bluetooth, LoRaWan o redes móviles (2G/3G/4G/5G).
Los microcontroladores ESP32-Wroom actuarán como nodos edge que procesarán los datos recolectados en tiempo real.


### 3. Gestión de Datos en el Fog (Capa de Preprocesamiento):
#### • Controladores Fog:
- Un dispositivo fog (puede ser un microcontrolador más robusto o un pequeño servidor local) gestionará la integración de los datos provenientes de múltiples nodos edge.
- Implementación de APIs para la comunicación entre los nodos edge y la capa de almacenamiento.


### 4. Transmisión y Almacenamiento de Datos:
- #### Optimización de la Transmisión:  
- Los datos preprocesados se transmiten eficientemente a la nube o a un servidor centralizado para su almacenamiento.
- Uso de técnicas para asegurar que solo los datos relevantes y necesarios se transmitan, optimizando el uso de ancho de banda y almacenamiento.


### 5. Monitoreo y Control Remoto:
- #### Plataforma en la Nube: 
- Un sistema centralizado que recibe, almacena y analiza los datos de glucosa en tiempo real. La plataforma proporciona acceso a los datos a los pacientes, cuidadores y profesionales de la salud a través de una aplicación móvil o web.

## TENTATIVA U OPTIMIZACION: 
- Aplicación Móvil: Una aplicación intuitiva que permite a los pacientes y médicos visualizar los niveles de glucosa, recibir alertas en caso de niveles críticos, y acceder a informes históricos y tendencias.

- Sistema de Alerta: Un sistema de notificación instantánea que envía alertas al paciente y al equipo médico en caso de que los niveles de glucosa se encuentren fuera del rango establecido.

## Impacto Esperado:

Este dispositivo IoT transformará la manera en que los pacientes diabéticos monitorean su condición, brindando una herramienta innovadora que no solo mejora el control de los niveles de glucosa, sino que también facilita la intervención médica oportuna y reduce las complicaciones asociadas con la diabetes.

## Beneficios:

Monitoreo Continuo: Permite la detección temprana de hiperglucemia o hipoglucemia, mejorando la calidad de vida de los pacientes y reduciendo el riesgo de complicaciones a largo plazo.
Conectividad: Los datos se transmiten en tiempo real a los profesionales de la salud, facilitando un seguimiento más cercano y personalizado.
Intervención Rápida: Las alertas automáticas permiten intervenciones inmediatas en situaciones de emergencia.
Mejora del Cumplimiento: Facilita a los pacientes mantener un registro constante de sus niveles de glucosa, promoviendo una mejor gestión de su condición.

## Objetivos del Proyecto:

Desarrollar un prototipo funcional del dispositivo IoT.
Integrar el sensor de glucosa con un módulo de conectividad confiable como por ejemplo el ESP32 Wroom.
Implementar la plataforma en la nube y la aplicación móvil o web para la visualización de datos.
Realizar pruebas piloto con pacientes diabéticos para validar la precisión y efectividad del sistema.
