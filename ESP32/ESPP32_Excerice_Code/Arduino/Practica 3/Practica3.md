- [Práctica: Configuración del ESP32 WROOM como Servidor Web (modo STA)](#práctica-configuración-del-esp32-wroom-como-servidor-web-modo-sta)
  - [1.0. Objetivo](#10-objetivo)
    - [1.1. Materiales necesarios](#11-materiales-necesarios)
    - [1.2. Conceptos previos](#12-conceptos-previos)
      - [1.2.1. Modo STA (Station)](#121-modo-sta-station)
      - [1.2.2. Servidor Web en ESP32](#122-servidor-web-en-esp32)
      - [1.2.3. GPIO2 o LED integrado](#123-gpio2-o-led-integrado)
    - [ESP32 Wi-Fi Modos de operación](#esp32-wi-fi-modos-de-operación)
    - [1.3 Procedimiento para probar](#13-procedimiento-para-probar)
    - [1.4 Preguntas para los alumnos](#14-preguntas-para-los-alumnos)
    - [1.5 Tarea (Extensión de la práctica)](#15-tarea-extensión-de-la-práctica)



# Práctica: Configuración del ESP32 WROOM como Servidor Web (modo STA)

## 1.0. Objetivo

Configurar el módulo ESP32 WROOM en modo Station (STA) para que se conecte a una red WiFi existente y funcione como servidor web.
El servidor permitirá encender o apagar el LED integrado de la placa mediante una interfaz web.

### 1.1. Materiales necesarios

- 1 módulo ESP32 WROOM (DEVKIT V1 o similar)

- 1 cable USB

- 1 computadora con Arduino IDE (versión con soporte para ESP32)

- Conexión WiFi disponible (SSID y contraseña)

### 1.2. Conceptos previos

#### 1.2.1. Modo STA (Station)
El ESP32 se conecta como un dispositivo cliente (como un celular o laptop) a una red WiFi existente.

#### 1.2.2. Servidor Web en ESP32
Permite que los usuarios accedan mediante un navegador (por IP) a una página HTML alojada en el ESP32, desde la cual se pueden enviar comandos (por ejemplo, encender o apagar un LED).

#### 1.2.3. GPIO2 o LED integrado
En la mayoría de las placas ESP32 el LED está conectado al **pin GPIO2** o **GPIO5**, dependiendo del modelo.  
(Se recomienda confirmar revisando el esquemático o probando directamente).

### ESP32 Wi-Fi Modos de operación
ESP32-STA-Mode.svg

<p align="center">
  <img src="ESP32-STA-Mode.svg" width="40%"><br>
  <em>Figura 1: ESP32 en modo STA </em>
</p>

|  **Modo**  | **Descripción**   | **Casos de uso**     |
|------------| ----------------- | ---------------------|
|Station Mode (STA) |Connects to a Wi-Fi network (like a router) and gets an IP address|IoT	Cloud	Communication, Web Server, Data Loggin| 
|Access Point Mode (AP) | Creates its own Wi-Fi network and allows other devices to connect.|Local	Communication,	IoT Mesh Network, Hotspot|
|Dual Mode (AP + STA) |Works as both an Access Point and a Station simultaneously.|IoT Gateway, Wi-Fi Extender, Smart Home Hub|



### 1.3 Procedimiento para probar

1. Cargar el código al ESP32.

2. Abrir el Monitor Serial (115200 baudios).

3. Esperar a que aparezca la línea con la IP del ESP32 (por ejemplo, 192.168.1.100).

4. En un navegador (del mismo WiFi), ingresar esa IP.

5. Verás una página con dos botones:

- **Encender LED**

-  **Apagar LED**

6. Al hacer clic, el LED en la placa debe cambiar su estado.

-------

### 1.4 Preguntas para los alumnos

1. ¿Cuál es la diferencia entre el modo STA y el modo AP en el ESP32?

2. ¿Qué función cumple 'WiFiServer' en este programa?

3. ¿Qué tipo de protocolo se usa para comunicar el navegador con el ESP32?

4. ¿Podrías modificar el código para controlar dos LEDs?

### 1.5 Tarea (Extensión de la práctica)

- Agregar un sensor (por ejemplo, DHT11 o LM35) y mostrar la lectura en la página web.

- Implementar control por AJAX (sin recargar la página).

- Cambiar a modo AP + STA para que el ESP32 cree su propia red y también se conecte a una existente.

