#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "honghui";
const char* password = "12345678";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");
  
  // Send HTTP GET request
  HTTPClient http;
  http.begin("http://localhost/traffic");  // Replace with your desired URL
  
  int httpResponseCode = http.POST();
  
  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    
    String payload = http.getString();
    Serial.println(payload);
  } else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  
  http.end();
}

void loop() {
  // Other code or actions to be performed can be added here
}
