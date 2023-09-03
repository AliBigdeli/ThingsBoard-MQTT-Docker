import paho.mqtt.publish as publish
import random
import json 



# MQTT broker details
broker_address = "localhost"  # Replace with your ThingsBoard MQTT broker address
broker_port = 1883  # Default MQTT port for ThingsBoard

# Access token of the device/entity in ThingsBoard
access_token = "thgkpgelq58omt9m7ze4"  # Replace with the actual access token

# MQTT topics
telemetry_topic = "v1/devices/me/telemetry"  # Telemetry topic for sending data to ThingsBoard


# Create a payload with the data to be sent
payload = {
    "temperature": random.randrange(25,30),
    "humidity": random.randrange(30,50),
    "pressure": random.randrange(900,1200)
}
payload_json = json.dumps(payload)

publish.single(
    telemetry_topic,
    payload=payload_json,
    hostname=broker_address,
    port=broker_port,
    auth={'username': access_token, 'password': ""}
)