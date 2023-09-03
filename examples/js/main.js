const mqtt = require("mqtt");

// MQTT broker details
const mqtt_server = "your_mqtt_broker_address";
const mqtt_port = 1883; // Default MQTT port for ThingsBoard

// Access token of the device/entity in ThingsBoard
const access_token = "your_device_access_token";

// MQTT topics
const telemetry_topic = "v1/devices/me/telemetry"; // Telemetry topic for sending data to ThingsBoard

// Create an MQTT client
const client = mqtt.connect(`mqtt://${mqtt_server}:${mqtt_port}`, {
  clientId: "jsClient",
  username: access_token,
});

// Handle MQTT client connection event
client.on("connect", () => {
  console.log("Connected to MQTT broker");

  // Send telemetry data to ThingsBoard
  sendTelemetryData();
});

// Handle MQTT client error event
client.on("error", (error) => {
  console.error("Error:", error);
});

// Send telemetry data to ThingsBoard
function sendTelemetryData() {
  // Generate random float values for temperature, humidity, and pressure
  const temperature = getRandomFloat(20, 30);
  const humidity = getRandomFloat(50, 70);
  const pressure = getRandomFloat(1000, 1020);

  // Create a payload with the random telemetry data
  const payload = JSON.stringify({ temperature, humidity, pressure });

  // Publish the telemetry data to ThingsBoard
  client.publish(telemetry_topic, payload, { qos: 1 }, (error) => {
    if (error) {
      console.error("Failed to send telemetry data:", error);
    } else {
      console.log("Telemetry data sent successfully");
    }

    // Disconnect from the MQTT broker after publishing the telemetry data
    client.end();
  });
}

// Utility function to generate random float values within a range
function getRandomFloat(min, max) {
  return Math.random() * (max - min) + min;
}
