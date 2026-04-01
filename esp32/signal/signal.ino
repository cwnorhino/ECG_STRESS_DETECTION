#include <WiFi.h>

const char *ssid = "Residency Flats";
const char *password = "suchimerapatih";

WiFiServer server(80);
WiFiClient client;

const int ecgPin = 34;

// AD8232 lead-off pins (if connected)
const int LO_PLUS = 32;
const int LO_MINUS = 33;

unsigned long lastSampleTime = 0;
const int sampleInterval = 4; // ~250 Hz

void setup()
{
  Serial.begin(115200);

  // ✅ ADC CONFIG (VERY IMPORTANT)
  analogReadResolution(12);                  // 0–4095
  analogSetAttenuation(ADC_11db);            // full range (0–3.3V)

  // Lead-off detection pins
  pinMode(LO_PLUS, INPUT);
  pinMode(LO_MINUS, INPUT);

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
  // Accept client
  if (!client || !client.connected())
  {
    client = server.available();
    return;
  }

  // ✅ PRECISE SAMPLING (better than delay)
  if (millis() - lastSampleTime >= sampleInterval)
  {
    lastSampleTime = millis();

    // ✅ Check electrode connection
    if (digitalRead(LO_PLUS) == 1 || digitalRead(LO_MINUS) == 1)
    {
      Serial.println("Leads off!");
      return;
    }

    // ✅ Read ECG with averaging
    int ecg = 0;
    for (int i = 0; i < 5; i++)   // increased smoothing
    {
      ecg += analogRead(ecgPin);
    }
    ecg /= 5;

    // Debug
    Serial.println(ecg);

    // Send over WiFi
    client.print(ecg);
    client.print("\n");
  }
}