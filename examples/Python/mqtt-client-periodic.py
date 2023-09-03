import paho.mqtt.client as mqtt
import random
import json
import time
from threading import Thread
# MQTT broker details
broker_address = "localhost"  # Replace with your ThingsBoard MQTT broker address
broker_port = 1883  # Default MQTT port for ThingsBoard

# Access token of the device/entity in ThingsBoard
access_token = "thgkpgelq58omt9m7ze4"  # Replace with the actual access token

# MQTT topics
# Telemetry topic for sending data to ThingsBoard
telemetry_topic = "v1/devices/me/telemetry"


def send_data(client):
    while True:
        # Create a payload with the data to be sent
        payload = {
            "temperature": random.randrange(25, 30),
            "humidity": random.randrange(30, 50),
            "pressure": random.randrange(900, 1200)
        }
        # Convert the payload to JSON format
        payload_json = json.dumps(payload)

        # sending the data to mqtt api
        client.publish(telemetry_topic, payload_json)

        # sleeping for 5 seconds to send another one
        time.sleep(5)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Publish the telemetry data to ThingsBoard
    Thread(target=send_data, args=(client, )).start()

    
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


# Connect to the MQTT broker
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username=access_token)
client.connect(broker_address, broker_port, 60)


client.loop_forever()
