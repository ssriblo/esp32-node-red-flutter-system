#include <WiFi.h>
#include <WebServer.h>

// Определяем SSID (имя сети Wi-Fi) и пароль для ESP32 в режиме точки доступа (SoftAP)
const char* ssid = "ESP32_Control"; // Имя Wi-Fi сети, которую будет создавать ESP32
const char* password = "your_password"; // Пароль для этой сети. Минимум 8 символов

// Создаем объект веб-сервера, слушающий на порту 80 (стандартный HTTP-порт)
WebServer server(80);

// Переменные для хранения полученных значений параметров
int param1 = 0;
int param2 = 0;
int param3 = 0;

// Обработчик для корневого URL ("/")
void handleRoot() {
  server.send(200, "text/plain", "Hello from ESP32!"); // Отправляем простое приветствие
}

// Обработчик для URL "/set_parameters"
void handleSetParameters() {
  Serial.println("Received request for /set_parameters");

  // Проверяем, есть ли параметры "p1", "p2", "p3" в запросе
  if (server.hasArg("p1") && server.hasArg("p2") && server.hasArg("p3")) {
    param1 = server.arg("p1").toInt(); // Извлекаем и преобразуем p1 в int
    param2 = server.arg("p2").toInt(); // Извлекаем и преобразуем p2 в int
    param3 = server.arg("p3").toInt(); // Извлекаем и преобразуем p3 в int

    // Выводим полученные значения в Serial Monitor для отладки
    Serial.print("Parameter 1: ");
    Serial.println(param1);
    Serial.print("Parameter 2: ");
    Serial.println(param2);
    Serial.print("Parameter 3: ");
    Serial.println(param3);

    // Отправляем успешный ответ обратно клиенту (Flutter-приложению)
    server.send(200, "text/plain", "Parameters received successfully!");
  } else {
    // Если параметры отсутствуют, отправляем ошибку
    server.send(400, "text/plain", "Error: Missing parameters p1, p2, or p3.");
    Serial.println("Error: Missing parameters in request.");
  }
}

// Обработчик для несуществующих страниц (404 Not Found)
void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  Serial.println(message);
}

void setup() {
  Serial.begin(115200); // Инициализация Serial Monitor

  // Выводим информацию о том, что ESP32 запускается как точка доступа
  Serial.print("Setting AP (Access Point)...");
  // Конфигурируем ESP32 как SoftAP
  // ESP32_Control - это SSID, your_password - пароль
  WiFi.softAP(ssid, password);

  // Получаем IP-адрес, присвоенный ESP32 в режиме SoftAP
  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP); // Обычно это 192.168.4.1

  // Регистрируем обработчики для различных URL
  server.on("/", handleRoot); // Обработчик для корневого URL
  server.on("/set_parameters", HTTP_GET, handleSetParameters); // Обработчик для URL, который будет принимать параметры

  // Регистрируем обработчик для несуществующих страниц
  server.onNotFound(handleNotFound);

  server.begin(); // Запускаем веб-сервер
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient(); // Обрабатываем входящие клиентские запросы
}
