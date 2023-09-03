#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Wi-Fi credentials
const char *ssid = "your_wifi_ssid";
const char *password = "your_wifi_password";

// MQTT broker details
const char *mqtt_server = "your_mqtt_broker_address";
const int mqtt_port = 1883; // Default MQTT port for ThingsBoard

// Access token of the device/entity in ThingsBoard
const char *access_token = "your_device_access_token";

// MQTT topics
const char *telemetry_topic = "v1/devices/me/telemetry"; // Telemetry topic for sending data to ThingsBoard

// Create an instance of the Wi-Fi client
WiFiClient wifiClient;

// Create an instance of the MQTT client
PubSubClient mqttClient(wifiClient);

// Connect to Wi-Fi
void connectToWiFi()
{
    Serial.print("Connecting to Wi-Fi...");
    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(1000);
        Serial.print(".");
    }

    Serial.println("\nConnected to Wi-Fi!");
}

// MQTT callback function
void mqttCallback(char *topic, byte *payload, unsigned int length)
{
    // Handle incoming MQTT messages if needed
}

// Connect to the MQTT broker
void connectToMQTTBroker()
{
    Serial.print("Connecting to MQTT broker...");
    while (!mqttClient.connected())
    {
        if (mqttClient.connect("arduinoClient", access_token, NULL))
        {
            Serial.println("\nConnected to MQTT broker!");

            // Subscribe to MQTT topics if needed
            // mqttClient.subscribe("your_topic");
        }
        else
        {
            Serial.print(".");
            delay(1000);
        }
    }
}

// Send telemetry data to ThingsBoard
void sendTelemetryData()
{
    // Create a payload with the data to be sent
    // Replace with your telemetry data
    // Generate random float values for temperature, humidity, and pressure
    float temperature = random(20, 30) + random(0, 9) / 10.0;
    float humidity = random(50, 70) + random(0, 9) / 10.0;
    float pressure = random(1000, 1020) + random(0, 9) / 10.0;

    // Create a payload with the random telemetry data
    String payload = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + ", \"pressure\": " + String(pressure) + "}";

    // Publish the telemetry data to ThingsBoard
    mqttClient.publish(telemetry_topic, payload.c_str());
}

void setup()
{
    Serial.begin(115200);

    // Connect to Wi-Fi
    connectToWiFi();

    // Set MQTT server and port
    mqttClient.setServer(mqtt_server, mqtt_port);

    // Set MQTT callback function
    mqttClient.setCallback(mqttCallback);
}

void loop()
{
    // Check if not connected to MQTT broker
    if (!mqttClient.connected())
    {
        // Connect to MQTT broker
        connectToMQTTBroker();
    }

    // Handle MQTT communication
    mqttClient.loop();

    // Send telemetry data to ThingsBoard
    sendTelemetryData();

    // Delay between telemetry data updates
    delay(5000);
}