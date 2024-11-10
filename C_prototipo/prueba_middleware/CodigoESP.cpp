#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "ssid";
const char* password = "contraseña";
const char* serverName = "http://<direccion-ip>:5000/middleware";  // Cambiar por la dirección IP del servidor

void setup() {
  Serial.begin(9600);
  
  // Conectar a WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando a WiFi...");
  }
  Serial.println("Conectado a WiFi");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverName);

    // Crear el JSON que se enviará desde el ESP32 - luego se reemplaza el código para que tome los datos directamente del sensor
    String postData = "{\"id_dispositivo\": \"ESP32_001\", \"valor_glucosa\": 95.3, \"fecha_lectura\": \"2024-10-04 12:00:00\"}";

    // Enviar la solicitud POST
    http.addHeader("Content-Type", "application/json");
    int httpResponseCode = http.POST(postData);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error en la solicitud POST: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(60000);  // Enviar datos cada 60 sec
}
