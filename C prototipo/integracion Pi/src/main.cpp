
#include <Arduino.h>
#include <WiFi.h>
#include <esp_sleep.h>
#include <EEPROM.h>
#include <HTTPClient.h>
#include <TFT_eSPI.h> 
#include <SPI.h>

// WiFi Configuration
const char* ssid = "Xiaomi";
const char* password = "12345678";

// Pin definitions for ESP32 WROOM
const int CAPACITIVO = 34;        // GPIO 34 - Touch 
const int CNY70 = 36;             // GPIO 36 
const int LED_ROJO = 26;          // GPIO 26
const int LED_VERDE = 27;         // GPIO 27

// Display SPI pins for ESP32 WROOM
#define TFT_MISO 19
#define TFT_MOSI 23
#define TFT_SCLK 18
#define TFT_CS   5  
#define TFT_DC   2
#define TFT_RST  4

// EEPROM 
const int EEPROM_SIZE = 512; 
int writeIndex = 0;

// Timing and state variables
unsigned long lastReadingTime = 0;
const unsigned long LECTURA_TIMEOUT = 10000;    // 10 seg
const unsigned long LED_BLINK_INTERVAL = 500;   // LED blink interval
unsigned long lastBlinkTime = 0;
bool leyendo = false;
unsigned long tiempoInicio = 0;
bool lecturaCompletada = false;

// ADC Config
const int ADC_RESOLUTION = 4095;    // ESP32 has 12-bit ADC
const float ADC_VOLTAGE = 3.3;      // Reference voltage

// TFT Disp
TFT_eSPI tft = TFT_eSPI();

// EEPROM
struct RegistroEstado {
    bool enviado;      // I
    unsigned long timestamp;
    unsigned short valor;
};

void setup() {
    Serial.begin(115200);
    
    //  ADC
    analogReadResolution(12);    
    analogSetAttenuation(ADC_11db); 
    
    // Init EEPROM
    if (!EEPROM.begin(EEPROM_SIZE)) {
        Serial.println("Failed to initialize EEPROM");
        while (1);
    }
    
    
    pinMode(CNY70, INPUT);
    pinMode(LED_ROJO, OUTPUT);
    pinMode(LED_VERDE, OUTPUT);
    
    // display
    tft.init();
    tft.setRotation(1);
    tft.fillScreen(TFT_BLACK);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);
    
    //  LED 
    digitalWrite(LED_ROJO, LOW);
    digitalWrite(LED_VERDE, LOW);
    
    //WiFi
    connectWiFi();
}

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

bool detectarContacto() {
    int touchValue = touchRead(CAPACITIVO);
    return touchValue < 40; 
}


void loop() {
    unsigned long currentTime = millis();
    bool contactoDetectado = detectarContacto();
    
    Serial.printf("Touch Value: %d, Contacto: %s\n", touchRead(CAPACITIVO), contactoDetectado ? "SI" : "NO");
    
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

void guardarMedicionEnEEPROM(unsigned long timestamp, int valor) {
    if (writeIndex >= EEPROM_SIZE - sizeof(RegistroEstado)) {
        writeIndex = 0;  
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