# Lectura de Sensor DHT22 con MicroPython

Este proyecto muestra cómo leer temperatura y humedad utilizando un **sensor DHT22** conectado a una tarjeta como **ESP32** o **ESP8266**, empleando MicroPython.

---

## Descripción

El programa inicializa el sensor DHT22 conectado al pin GPIO 15 y realiza lecturas periódicas de temperatura y humedad cada 2 segundos. También implementa un bloque `try/except` para manejar errores comunes en la comunicación con el sensor.

---

## Código

```python
import dht
from machine import Pin
import time

sensor = dht.DHT22(Pin(15))

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        humidity = sensor.humidity()
        print(f'Temperature: {temp} C degree Humidity: {humidity} %')
    except OSError as e:
        print('Failed to read Sensor')

    time.sleep(2)
```

## Explicación del Programa

1. Importación de módulos

dht → Control del sensor DHT11/DHT22.

machine.Pin → Control de pines GPIO del microcontrolador.

time → Se usa para generar pausas entre lecturas.

Explicación del Programa
1. Importación de módulos

- dht → Control del sensor DHT11/DHT22.

- machine.Pin → Control de pines GPIO del microcontrolador.

- time → Se usa para generar pausas entre lecturas.

```python
import dht
from machine import Pin
import time
```

2. Configuración del sensor

```python
sensor = dht.DHT22(Pin(15))
```

Crea un objeto sensor de tipo DHT22, indicando que está conectado al GPIO 15.
Si el sensor está en otro pin, simplemente cámbialo.

3. Ciclo de lectura

```python
sensor = dht.DHT22(Pin(15))
```

El programa entra en un bucle infinito para leer el sensor periódicamente.

4. Lectura de datos y manejo de errores

```python
try:
    sensor.measure()
    temp = sensor.temperature()
    humidity = sensor.humidity()
    print(f'Temperature: {temp} C degree Humidity: {humidity} %')
except OSError as e:
    print('Failed to read Sensor')
```

- `sensor.measure()` realiza una nueva medición.

- `sensor.temperature()` devuelve la temperatura en °C.

- `sensor.humidity()` retorna la humedad %.

- `except captura errores comunes` (mal cableado, ruido eléctrico, ausencia del sensor).

5. Tiempo de espera entre mediciones

```python
time.sleep(2)
```

El sensor DHT22 requiere al menos 2 segundos entre lecturas, por lo que esta demora garantiza lecturas correctas.