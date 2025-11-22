# Enviando datos a un Broker MQTT

import network  #Módulo de MicroPython para manejar interfaces de red (WiFi, Ethernet, etc.)
from umqtt.simple import MQTTClient
import time
import dht
import ujson
from machine import Pin

MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi-weather"

sensor = dht.DHT22(Pin(15))

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print("Connecting to WIFI.....",end="")
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)

print('\n Connected!')
print('Network config;',sta_if.ifconfig())

client = MQTTClient(MQTT_CLIENT_ID,MQTT_BROKER)
client.connect()
print("Connected to MQTT Boker")

prev_weather =""
while True:
    sensor.measure()
    message = ujson.dumps({"temp": sensor.temperature(),
                           "humidity": sensor.humidity(),})
    if message !=prev_weather:
        print(f"Publishing: {message}")
        client.publish(MQTT_TOPIC,message)
        prev_weather = message
    else:
        print("No change in weather condition")

    time.sleep(2)
