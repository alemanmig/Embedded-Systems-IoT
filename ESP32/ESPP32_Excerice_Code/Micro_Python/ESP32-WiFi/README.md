# Conexión WiFi en MicroPython (ESP32/ESP8266)

Este documento explica cómo conectar un microcontrolador como el **ESP32** o **ESP8266** a una red WiFi utilizando MicroPython.  
El código establece la interfaz WiFi, inicia la conexión y espera hasta que el dispositivo obtenga una dirección IP.

---

## Código de Ejemplo

```python
import network
import time

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
print("Connecting to WIFI.....", end="")
sta_if.connect('Wokwi-GUEST', '')

while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)

print('\n Connected!')
print('Network config;', sta_if.ifconfig())
```

## Explicación del Código

1. Importación de módulos

network → Maneja interfaces de red como WiFi.

time → Permite pausas durante la conexión.

```python
import network
import time
```

2. Configurar interfaz WiFi en modo estación

```python
sta_if = network.WLAN(network.STA_IF)
```

MicroPython soporta dos modos:

STA_IF (Station) → El módulo se conecta a un router WiFi.

AP_IF (Access Point) → El módulo crea su propia red WiFi.

En este caso, usamos Station Mode, el más común para conectarse a internet.

3. Activar la interfaz WiFi

```python
sta_if.active(True)
```

Enciende el módulo WiFi.
Si se deseara apagar, se usaría False.

4. Iniciar conexión a la red

```python
sta_if.connect('Wokwi-GUEST', '')
```

Argumentos:

Nombre de la red (SSID)

Contraseña (vacía en redes abiertas)

Este ejemplo usa "Wokwi-GUEST", que no requiere password.

5. Esperar hasta que la conexión se establezca

```python
while not sta_if.isconnected():
    print('.', end='')
    time.sleep(0.5)
```

El ciclo verifica continuamente si el WiFi ya está conectado.

Muestra puntos en la terminal para indicar progreso.

Espera 0.5 segundos entre intentos.

Esto evita que el programa avance sin conexión.

6. Mostrar información de red

```python
print('\n Connected!')
print('Network config;', sta_if.ifconfig())
```

Una vez conectado, se imprime:

Mensaje de conexión exitosa.

Configuración IP del dispositivo:

ifconfig() devuelve una tupla:

Dirección IP

Máscara de red

Puerta de enlace

Servidor DNS

Ejemplo:

```python
('192.168.1.34', '255.255.255.0', '192.168.1.1', '8.8.8.8')
```

### Notas adicionales

El ESP32 tarda algunos segundos en conectarse dependiendo de la intensidad de la señal.

Este código debe ser ejecutado antes de cualquier comunicación por internet (HTTP, MQTT, sockets, etc.).

Se puede reutilizar dentro de proyectos IoT que requieran conectividad.