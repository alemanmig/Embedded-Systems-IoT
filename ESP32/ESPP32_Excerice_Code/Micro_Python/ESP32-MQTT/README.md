# Envío de Datos a un Broker MQTT con MicroPython (ESP32/ESP8266)

Este proyecto muestra cómo conectar un microcontrolador **ESP32** o **ESP8266** a una red WiFi, leer datos de un sensor **DHT22** y enviarlos en formato **JSON** a un broker MQTT público.  
Es un ejemplo típico de un sistema **IoT** real usando MicroPython.

---

## Requisitos

- ESP32 o ESP8266 con MicroPython instalado  
- Sensor **DHT22** conectado a GPIO 15  
- Conexión WiFi  
- Un broker MQTT público (en este caso: `broker.mqttdashboard.com`)

---

## Código completo

```python
# Enviando datos a un Broker MQTT

import network
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
print("Connecting to WIFI.....", end="")
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)

print('\n Connected!')
print('Network config:', sta_if.ifconfig())

client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.connect()
print("Connected to MQTT Broker")

prev_weather = ""
while True:
    sensor.measure()
    message = ujson.dumps({
        "temp": sensor.temperature(),
        "humidity": sensor.humidity(),
    })

    if message != prev_weather:
        print(f"Publishing: {message}")
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
    else:
        print("No change in weather condition")

    time.sleep(2)
```

## Explicación del Programa

1. Importación de módulos

| Módulo       | Función                     |
| ------------ | --------------------------- |
| `network`    | Manejo del WiFi             |
| `MQTTClient` | Cliente MQTT ligero         |
| `time`       | Pausas y temporización      |
| `dht`        | Lectura de sensores DHT22   |
| `ujson`      | Conversión a JSON eficiente |
| `Pin`        | Control de pines GPIO       |

2. Configuración MQTT

```python
MQTT_CLIENT_ID = "micropython-weather-demo"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi-weather"
```

- CLIENT_ID identifica tu dispositivo.

- BROKER es el servidor MQTT.

- TOPIC es donde publicas los datos.

3. Inicialización del sensor DHT22

```python
sensor = dht.DHT22(Pin(15))
```
El DHT22 está conectado al GPIO 15.

4. Conexión a WiFi

```python
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Wokwi-GUEST', '')
```

- Usa modo estación (`STA_IF`).
- Se conecta a una red abierta.

El código espera la conexión:

```python
while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)
```

Al conectarse, imprime la configuración IP:

```python
sta_if.ifconfig()
```

5. Conexión al broker MQTT

```python
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER)
client.connect()
```

Si esta línea no falla, el dispositivo está conectado al broker.

6. Bucle principal: lectura + publicación
### Medición del sensor

```python
sensor.measure()
```

### Crear un mensaje JSON

```python
message = ujson.dumps({
    "temp": sensor.temperature(),
    "humidity": sensor.humidity(),
})
```

Ejemplo:

```python
{"temp": 24.1, "humidity": 52.3}
```

### Publicar solo si cambiaron los datos

```python
if message != prev_weather:
    client.publish(MQTT_TOPIC, message)
    prev_weather = message
```

Esto evita tráfico innecesario.

## Flujo de funcionamiento
1. Conecta el ESP32/ESP8266 a WiFi
2. Conecta al broker MQTT
3. Lee sensor DHT22
4. Crea JSON
5. Publica el JSON si hubo cambios
6. Repite cada 2 segundos

## Posibles mejoras

- Añadir reconexión automática a WiFi
- Reconexión al broker si se pierde la sesión
- Uso de TLS/SSL para seguridad
- Guardar datos en una base local (SD o SPIFFS)
- Enviar alertas (temperatura alta, humedad baja)

## Visualización de datos

Puedes visualizar los datos con:

- MQTT Explorer
- Node-RED Dashboard
- ThingsBoard
- Home Assistant

Solo necesitas suscribirte al topic:

```
wokwi-weather
```