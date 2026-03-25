#include <WiFi.h>

const char *ssid = "hahawifi";
const char *password = "haharight";

WiFiServer server(80);
WiFiClient client;

const int ecgPin = 34;

void setup()
{
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("ESP32 IP: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop()
{

  // 🔥 accept client only once
  if (!client || !client.connected())
  {
    client = server.available();
    return;
  }

  // 🔥 read ECG (light smoothing)
  int ecg = 0;
  for (int i = 0; i < 3; i++)
  {
    ecg += analogRead(ecgPin);
  }
  ecg /= 3;

  // debug on serial plotter
  Serial.println(ecg);

  // 🔥 send continuously
  client.print(ecg);
  client.print("\n");

  delay(4); // ~250 Hz
}