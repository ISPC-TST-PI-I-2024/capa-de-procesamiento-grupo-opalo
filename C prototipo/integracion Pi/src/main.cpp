#include <Arduino.h>
#include <WiFi.h>
#include <esp_sleep.h>
#include <EEPROM.h>
#include <HTTPClient.h>
#include <TFT_eSPI.h> 
#include <SPI.h>

// Configuración WiFi
const char* ssid = "Xiaomi";
const char* password = "12345678";

// Definición de pines para ESP32 WROOM
const int CAPACITIVO = 34;        // GPIO 34 - Sensor Touch 
const int CNY70 = 36;             // GPIO 36 - Sensor CNY70
const int LED_ROJO = 26;          // GPIO 26 - LED Indicador
const int LED_VERDE = 27;         // GPIO 27 - LED Indicador

// Pines SPI para pantalla TFT en ESP32 WROOM
#define TFT_MISO 19
#define TFT_MOSI 23
#define TFT_SCLK 18
#define TFT_CS   5  
#define TFT_DC   2
#define TFT_RST  4

// Configuración EEPROM 
const int EEPROM_SIZE = 512; 
int writeIndex = 0;

// Variables de tiempo y estado
unsigned long lastReadingTime = 0;
const unsigned long LECTURA_TIMEOUT = 10000;    // 10 segundos timeout
const unsigned long LED_BLINK_INTERVAL = 500;   // Intervalo parpadeo LED
unsigned long lastBlinkTime = 0;
bool leyendo = false;
unsigned long tiempoInicio = 0;
bool lecturaCompletada = false;

// Configuración ADC
const int ADC_RESOLUTION = 4095;    // ESP32 tiene ADC de 12 bits
const float ADC_VOLTAGE = 3.3;      // Voltaje de referencia

// Objeto pantalla TFT
TFT_eSPI tft = TFT_eSPI();

// Estructura para almacenar datos en EEPROM
struct RegistroEstado {
    bool enviado;                // Indicador si fue enviado
    unsigned long timestamp;     // Marca de tiempo
    unsigned short valor;        // Valor medido
};

// Función de inicialización
void setup() {
    Serial.begin(115200);
    
    // Configuración ADC
    analogReadResolution(12);    
    analogSetAttenuation(ADC_11db); 
    
    // Inicializar EEPROM
    if (!EEPROM.begin(EEPROM_SIZE)) {
        Serial.println("Error al inicializar EEPROM");
        while (1);
    }
    
    // Configurar pines
    pinMode(CNY70, INPUT);
    pinMode(LED_ROJO, OUTPUT);
    pinMode(LED_VERDE, OUTPUT);
    
    // Inicializar pantalla
    tft.init();
    tft.setRotation(1);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    
    // Estado inicial LEDs
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, LOW);
    
    // Conectar WiFi
    connectWiFi();
}

// Función para conectar WiFi
void connectWiFi() {
    Serial.println("Conectando a WiFi...");
    WiFi.begin(ssid, password);
    
    int intentos = 0;
    while (WiFi.status() != WL_CONNECTED && intentos < 40) {
        delay(500);
        Serial.print(".");
        intentos++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nConectado a WiFi");
        Serial.print("Dirección IP: ");
        Serial.println(WiFi.localIP());
    } else {
        Serial.println("\nFalló la conexión WiFi");
    }
}

// Función para leer sensor CNY70
float leerCNY70() {
    const int NUMERO_MUESTRAS = 10;
    long suma = 0;
    
    for(int i = 0; i < NUMERO_MUESTRAS; i++) {
        suma += analogRead(CNY70);
        delay(10);
    }
    
    float promedio = suma / NUMERO_MUESTRAS;
    float voltaje = (promedio * ADC_VOLTAGE) / ADC_RESOLUTION;
    
    Serial.printf("Valor ADC: %.2f, Voltaje: %.2f V\n", promedio, voltaje);
    return voltaje;
}

// Función para detectar contacto capacitivo
bool detectarContacto() {
    int touchValue = touchRead(CAPACITIVO);
    return touchValue < 40; 
}

// Función para mostrar lectura en pantalla
void mostrarLectura(float valor) {
    tft.fillScreen(TFT_BLACK);
    tft.setTextSize(2);
    
    // Mostrar título
    tft.setCursor(10, 10);
    tft.println("Resultado de lectura:");
    
    // Mostrar valor
    tft.setCursor(10, 40);
    tft.setTextSize(3);
    tft.printf("%.2f V", valor);
    
    // Mostrar estado
    tft.setTextSize(2);
    tft.setCursor(10, 80);
    tft.println("Estado: Completado");
    
    // Mostrar timestamp
    tft.setCursor(10, 110);
    tft.setTextSize(1);
    unsigned long tiempoTranscurrido = millis() / 1000;
    tft.printf("Tiempo: %02lu:%02lu:%02lu", 
        tiempoTranscurrido / 3600,
        (tiempoTranscurrido % 3600) / 60,
        tiempoTranscurrido % 60
    );
}

// Función para guardar medición en EEPROM
void guardarMedicionEnEEPROM(unsigned long timestamp, int valor) {
    if (writeIndex >= EEPROM_SIZE - sizeof(RegistroEstado)) {
        writeIndex = 0;  // Volver al inicio si se llena
    }
    
    RegistroEstado registro;
    registro.enviado = false;
    registro.timestamp = timestamp;
    registro.valor = valor;
    
    EEPROM.put(writeIndex, registro);
    
    if (EEPROM.commit()) {
        Serial.println("Datos guardados en EEPROM");
        writeIndex += sizeof(RegistroEstado);
    } else {
        Serial.println("Error al guardar en EEPROM");
    }
}

// Función para enviar datos al servidor
void enviarDatosAlServidor() {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("Sin conexión WiFi");
        return;
    }

    HTTPClient http;
    http.begin("http://192.168.0.10:5000/api/mediciones");
    http.addHeader("Content-Type", "application/json");
    
    int registrosEnviados = 0;
    
    for (int i = 0; i < writeIndex; i += sizeof(RegistroEstado)) {
        RegistroEstado registro;
        EEPROM.get(i, registro);
        
        if (!registro.enviado) {
            String jsonData = "{\"timestamp\":" + String(registro.timestamp) + 
                            ",\"valor\":" + String(registro.valor/100.0, 2) + "}";
            
            int httpCode = http.POST(jsonData);
            
            if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_CREATED) {
                registro.enviado = true;
                EEPROM.put(i, registro);
                registrosEnviados++;
                Serial.printf("Registro enviado exitosamente. Timestamp: %lu\n", registro.timestamp);
            } else {
                Serial.printf("Error al enviar registro. HTTP code: %d\n", httpCode);
                break;
            }
            delay(100);
        }
    }
    
    http.end();
    
    if (registrosEnviados > 0 && EEPROM.commit()) {
        Serial.printf("Se marcaron %d registros como enviados\n", registrosEnviados);
    } else {
        Serial.println("Error al actualizar estado de registros en EEPROM");
    }
}

// Función para entrar en modo bajo consumo
void entrarModoBajoConsumo() {
    Serial.println("Entrando en modo de bajo consumo...");
    
    // Apagar LEDs
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, LOW);
    
    // Mostrar mensaje en pantalla
    tft.fillScreen(TFT_BLACK);
    tft.setTextSize(2);
    tft.setCursor(10, 10);
    tft.println("Modo de bajo consumo");
    tft.setTextSize(1);
    tft.setCursor(10, 40);
    tft.println("Toque el sensor para");
    tft.setCursor(10, 55);
    tft.println("realizar nueva lectura");
    
    // Configurar despertar por touch
    touchAttachInterrupt(CAPACITIVO, [](){}, 40);
    esp_sleep_enable_touchpad_wakeup();
    
    delay(2000);
    esp_deep_sleep_start();
}

// Bucle principal
void loop() {
    unsigned long currentTime = millis();
    bool contactoDetectado = detectarContacto();
    
    Serial.printf("Valor Touch: %d, Contacto: %s\n", 
                 touchRead(CAPACITIVO), 
                 contactoDetectado ? "SI" : "NO");
    
    if (contactoDetectado && !leyendo) {
        leyendo = true;
        tiempoInicio = currentTime;
        lecturaCompletada = false;
        digitalWrite(LED_ROJO, LOW);
        Serial.println("Contacto detectado - Iniciando lectura");
    }
    
    if (leyendo) {
        if (!contactoDetectado) {
            leyendo = false;
            digitalWrite(LED_VERDE, LOW);
            digitalWrite(LED_ROJO, HIGH);
            Serial.println("Contacto perdido durante lectura");
            return;
        }
        
        if (currentTime - lastBlinkTime >= LED_BLINK_INTERVAL) {
            digitalWrite(LED_VERDE, !digitalRead(LED_VERDE));
            lastBlinkTime = currentTime;
            float valorActual = leerCNY70();
            Serial.printf("Lectura en curso: %.2f V\n", valorActual);
        }
        
        if (currentTime - tiempoInicio >= LECTURA_TIMEOUT && !lecturaCompletada) {
            lecturaCompletada = true;
            digitalWrite(LED_VERDE, HIGH);
            
            float valorFinal = leerCNY70();
            guardarMedicionEnEEPROM(currentTime, valorFinal * 100);
            mostrarLectura(valorFinal);
            
            if (WiFi.status() == WL_CONNECTED) {
                enviarDatosAlServidor();
            } else {
                Serial.println("Sin conexión WiFi - Datos guardados en EEPROM");
                connectWiFi();
            }
            
            delay(3000);
            entrarModoBajoConsumo();
        }
    } else {
        digitalWrite(LED_VERDE, LOW);
        if (currentTime - lastBlinkTime >= LED_BLINK_INTERVAL) {
            digitalWrite(LED_ROJO, !digitalRead(LED_ROJO));
            lastBlinkTime = currentTime;
        }
    }
}