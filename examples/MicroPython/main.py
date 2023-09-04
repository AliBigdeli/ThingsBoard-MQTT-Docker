import network
from machine import Pin ,reset,Timer
from time import sleep
from umqtt import MQTTClient
import ujson
import random
import dht

# wifi conenction credentials
SSID = "wifi ssid"
PASSWORD = "wifi pass"

# MQTT Server Parameters
MQTT_CLIENT_ID = "promake-demo"
MQTT_BROKER    = "test.mosquitto.org"
MQTT_USER      = ""
MQTT_PASSWORD  = ""
MQTT_TOPIC     = "v1/devices/me/telemetry"

wlan_sta = network.WLAN(network.STA_IF)
wlan_sta.active(True)
wlan_sta.connect(SSID, PASSWORD)

print("trying to connect to wifi")
while not wlan_sta.isconnected():
    pass


# pin setup
relay_pin = Pin(26, Pin.OUT)
dht11_pin = Pin(5, Pin.IN)
dht11 = dht.DHT11(dht11_pin)
relay_pin.off()

# setup the timer
timer = Timer(0)

def sub_callback(topic, msg):
  print((topic, msg))
  
    
def connect_and_subscribe():
  client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER,user=MQTT_USER,password=MQTT_PASSWORD)
  client.set_callback(sub_callback)
  client.connect()
  client.subscribe(MQTT_TOPIC)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_BROKER, MQTT_TOPIC))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  sleep(10)
  reset()
  
try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()

def get_states(timer):
  dht11.measure()
  temp = dht11.temperature()
  humidity = dht11.humidity()
  client.publish(MQTT_TOPIC,ujson.dumps({"temperature":temp,"humidity":humidity}))
  

timer.init(period=3000, callback=get_states)


while True:
  try:
    client.check_msg()
  except OSError as e:
    restart_and_reconnect()