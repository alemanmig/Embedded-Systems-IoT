# Conexion a WiFi de la ESP32

import network  #Módulo de MicroPython para manejar interfaces de red (WiFi, Ethernet, etc.)

import time

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print("Connecting to WIFI.....",end="")
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)

print('\n Connected!')
print('Network config;',sta_if.ifconfig())