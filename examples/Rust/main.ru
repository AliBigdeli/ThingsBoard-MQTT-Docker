use rand::Rng;
use rumqttc::{Client, MqttOptions, QoS};

// MQTT broker details
const MQTT_SERVER: &str = "your_mqtt_broker_address";
const MQTT_PORT: u16 = 1883; // Default MQTT port for ThingsBoard
const ACCESS_TOKEN: &str = "your_device_access_token";

// MQTT topics
const TELEMETRY_TOPIC: &str = "v1/devices/me/telemetry"; // Telemetry topic for sending data to ThingsBoard

// Generate random float values for temperature, humidity, and pressure
fn generate_telemetry_data() -> (f32, f32, f32) {
    let mut rng = rand::thread_rng();
    let temperature = rng.gen_range(20.0..30.0);
    let humidity = rng.gen_range(50.0..70.0);
    let pressure = rng.gen_range(1000.0..1020.0);
    (temperature, humidity, pressure)
}

// Send telemetry data to ThingsBoard
fn send_telemetry_data(client: &mut Client) {
    let (temperature, humidity, pressure) = generate_telemetry_data();

    // Create a payload with the random telemetry data
    let payload = format!(
        r#"{{"temperature": {}, "humidity": {}, "pressure": {}}}"#,
        temperature, humidity, pressure
    );

    // Publish the telemetry data to ThingsBoard
    client
        .publish(TELEMETRY_TOPIC, QoS::AtLeastOnce, false, payload)
        .unwrap();
}

fn main() {
    // Create MQTT client options
    let mqtt_options = MqttOptions::new("rustClient", MQTT_SERVER, MQTT_PORT).set_keep_alive(5);

    // Create an MQTT client
    let (mut client, _) = Client::new(mqtt_options, 10);

    // Connect to the MQTT broker
    client
        .connect(None)
        .expect("Failed to connect to MQTT broker");

    // Send telemetry data to ThingsBoard
    send_telemetry_data(&mut client);

    // Disconnect from the MQTT broker
    client.disconnect().unwrap();
}