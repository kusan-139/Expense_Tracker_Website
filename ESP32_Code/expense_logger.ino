#include <WiFi.h>
#include <HTTPClient.h>
#include "time.h"

const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";

const char* serverURL = "http://192.168.1.4:5000/add";  // Replace with your PC IP

const int foodBtn = 4;
const int travelBtn = 5;

const char* ntpServer = "pool.ntp.org";
const long gmtOffset_sec = 19800;   // IST timezone (5:30)
const int daylightOffset_sec = 0;

void sendExpense(String category, int amount) {

  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return;
  }

  char dateStr[20];
  strftime(dateStr, sizeof(dateStr), "%Y-%m-%d", &timeinfo);

  int month = timeinfo.tm_mon + 1;

  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;
    http.begin(serverURL);
    http.addHeader("Content-Type", "application/json");

    String jsonData = "{";
    jsonData += "\"category\":\"" + category + "\",";
    jsonData += "\"amount\":" + String(amount) + ",";
    jsonData += "\"type\":\"Expense\",";
    jsonData += "\"date\":\"" + String(dateStr) + "\",";
    jsonData += "\"month\":" + String(month) + ",";
    jsonData += "\"device\":\"ESP32-01\"";
    jsonData += "}";

    int httpResponseCode = http.POST(jsonData);

    Serial.print("HTTP Response: ");
    Serial.println(httpResponseCode);

    http.end();
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(foodBtn, INPUT);
  pinMode(travelBtn, INPUT);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("WiFi Connected!");

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {

  if (digitalRead(foodBtn) == HIGH) {
    sendExpense("Food", 100);
    delay(500);
  }

  if (digitalRead(travelBtn) == HIGH) {
    sendExpense("Travel", 150);
    delay(500);
  }
}