# Red LoRaWAN Local con IoT — Proyecto IPN

Red LoRaWAN local para enseñanza de IoT sin depender de internet, basada en el gateway Laird Sentrius RG191, la placa Heltec WiFi LoRa 32 V3, y Raspberry Pi 5 como servidor.

---

## Arquitectura del sistema

```
Heltec WiFi LoRa 32 V3 (nodo + DHT11)
        ↓  LoRa 915 MHz
Laird Sentrius RG191 (gateway)
        ↓  UDP Semtech :1700
Raspberry Pi 5 — 192.168.0.45
  ├── ChirpStack v4      → :8080  (servidor LoRaWAN)
  ├── Mosquitto MQTT     → :1883  (broker IoT)
  ├── ChirpStack Gateway Bridge (puente UDP↔MQTT)
  └── Node-RED           → :1880  (dashboard visualización)
```

---

## Hardware utilizado

| Componente | Modelo | Notas |
|---|---|---|
| Gateway LoRaWAN | Laird Sentrius RG191 | US915, firmware 3.5.0.10022 |
| Nodo LoRa | Heltec WiFi LoRa 32 V3 | ESP32-S3 + SX1262 + OLED integrado |
| Sensor | DHT11 | Temperatura y humedad, conectado a GPIO 48 (3.3V) |
| Servidor de red | Raspberry Pi 5 | Debian 13 Trixie |

---

## 1. Configuración del Gateway Laird Sentrius RG191

### Conexión inicial

1. Conectar las 3 antenas:
   - 2 antenas cortas → puertos WiFi (2.4/5.5 GHz)
   - 1 antena larga → puerto LoRa (900 MHz)
2. Conectar cable Ethernet al router
3. Conectar fuente de poder

### Acceso al panel web

La URL usa los últimos 6 dígitos de la MAC (en la etiqueta del fondo):

```
https://rg1xx2984C7.local
```

> Si `.local` no resuelve, busca la IP en el panel DHCP de tu router.

Credenciales por defecto:
```
Usuario:  sentrius
Password: RG1xx
```

### Configuración LoRa para red local

1. Ir a **LoRa → Presets** → seleccionar **TTN Legacy US** → Apply
2. Ir a **LoRa → Advanced** → **Save current LoRa Configuration**
3. Editar el archivo JSON descargado — cambiar únicamente:

```json
"lora": {
    "logging_level": "debug",
    "gateway_mode": "semtech"
},
"forwarder": {
    "server_address": "192.168.0.45",
    "serv_port_up": 1700,
    "serv_port_down": 1700,
    "keepalive_interval": 10,
    "stat_interval": 30,
    "push_timeout_ms": 100,
    "forward_crc_valid": true,
    "forward_crc_error": false,
    "forward_crc_disabled": false
}
```

4. Ir a **LoRa → Advanced** → **Upload and save LoRa Configuration** → subir el archivo editado

> ⚠️ Asegurarse que `gateway_mode` sea `"semtech"` (no `"mqtt"`). Si se sube el JSON sin este campo, el gateway cambia a modo MQTT y deja de funcionar con ChirpStack.

### Gateway EUI

El EUI del gateway (necesario para registrarlo en ChirpStack):
```
c0ee40ffff2984c7
```

---

## 2. Configuración del Raspberry Pi 5

### Sistema operativo
- Debian GNU/Linux 13 (Trixie)
- IP estática: `192.168.0.45`

### IP estática

Editar `/etc/dhcpcd.conf`:

```
interface eth0
static ip_address=192.168.0.45/24
static routers=192.168.0.1
static domain_name_servers=192.168.0.1
```

---

## 3. Instalación de Mosquitto MQTT

```bash
sudo apt update && sudo apt install -y mosquitto mosquitto-clients

# Crear directorios necesarios
sudo mkdir -p /var/log/mosquitto /run/mosquitto /var/lib/mosquitto
sudo chown mosquitto /var/log/mosquitto /run/mosquitto /var/lib/mosquitto
```

Configuración en `/etc/mosquitto/conf.d/mosquitto.conf`:
```
listener 1883 0.0.0.0
allow_anonymous true
```

```bash
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

> **Nota:** Al instalar ChirpStack con Docker, Mosquitto del sistema se deshabilita y Docker usa su propio contenedor Mosquitto en el mismo puerto 1883.

### Prueba de funcionamiento

```bash
# Terminal 1 — suscribirse
mosquitto_sub -h 127.0.0.1 -p 1883 -t "test"

# Terminal 2 — publicar
mosquitto_pub -h 127.0.0.1 -p 1883 -t "test" -m "hola"
```

---

## 4. Instalación de ChirpStack con Docker

### Prerequisitos

```bash
# Docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER
newgrp docker

# Docker Compose plugin
sudo apt install -y docker-compose-plugin
```

### Descargar ChirpStack Docker

```bash
cd ~
git clone https://github.com/chirpstack/chirpstack-docker.git
cd chirpstack-docker
```

### Configuración para US915 (México)

**1. Editar `docker-compose.yml`** — cambiar topics del `chirpstack-gateway-bridge`:

```yaml
environment:
  - INTEGRATION__MQTT__EVENT_TOPIC_TEMPLATE=us915_0/gateway/{{ .GatewayID }}/event/{{ .EventType }}
  - INTEGRATION__MQTT__STATE_TOPIC_TEMPLATE=us915_0/gateway/{{ .GatewayID }}/state/{{ .StateType }}
  - INTEGRATION__MQTT__COMMAND_TOPIC_TEMPLATE=us915_0/gateway/{{ .GatewayID }}/command/#
```

Y cambiar el basicstation a us915:
```yaml
command: -c /etc/chirpstack-gateway-bridge/chirpstack-gateway-bridge-basicstation-us915_0.toml
```

**2. Habilitar región US915 en `configuration/chirpstack/chirpstack.toml`:**

```toml
enabled_regions=["us915_0"]
```

**3. Deshabilitar Mosquitto del sistema** (Docker usa el suyo):

```bash
sudo systemctl stop mosquitto
sudo systemctl disable mosquitto
```

### Levantar ChirpStack

```bash
docker compose up -d
```

Verificar que todos los servicios estén corriendo:
```bash
docker compose ps
```

Servicios esperados:
| Servicio | Puerto | Estado |
|---|---|---|
| chirpstack | 8080 | Up |
| chirpstack-gateway-bridge | 1700/udp | Up |
| chirpstack-rest-api | 8090 | Up |
| mosquitto | 1883 | Up |
| postgres | 5432 | Up |
| redis | 6379 | Up |

### Panel de administración

```
URL:      http://192.168.0.45:8080
Usuario:  admin
Password: admin
```

---

## 5. Registro del gateway en ChirpStack

1. Ir a **Gateways → Add gateway**
2. Llenar:
   - **Name:** `sentrius-laird`
   - **Gateway EUI:** `c0ee40ffff2984c7`
3. Guardar

El gateway debe aparecer como **online** una vez que el Sentrius esté apuntando al Pi 5.

---

## 6. Configuración del nodo Heltec WiFi LoRa 32 V3

### Prerequisitos Arduino IDE

1. Agregar URL en **Preferences → Additional Boards Manager URLs:**
   ```
   https://resource.heltec.cn/download/package_heltec_esp32_index.json
   ```
2. Instalar **Heltec ESP32 Series Dev-boards** en Boards Manager
3. Instalar librería **RadioLib** (by Jan Gromes) v7.7.0 en Library Manager
4. Instalar librería **DHT sensor library** (by Adafruit) en Library Manager
5. Seleccionar placa: **Tools → Board → WiFi LoRa 32(V3)**

### Conexión del sensor DHT11

| DHT11 | Heltec WiFi LoRa 32 V3 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| DATA | GPIO 48 |

> El DHT11 funciona con 3.3V y 5V. Se recomienda 3.3V para compatibilidad directa con el ESP32.

### Credenciales del dispositivo en ChirpStack

| Campo | Valor |
|---|---|
| **Device EUI** | `17c09b9ebf474ada` |
| **Join EUI** | `4aca057b56a0ab4c` |
| **Application Key** | `66450b8ad90d705d94025a4fb2866bd6` |

### Registro en ChirpStack

1. **Device Profiles → Add device profile:**
   - Name: `heltec-us915-otaa`
   - Region: `US915`
   - MAC version: `LoRaWAN 1.0.3`
   - Activation: `OTAA`

2. **Applications → Add application:**
   - Name: `iot-local-ipn`

3. **Applications → iot-local-ipn → Add device:**
   - Name: `heltec-lora32-v3`
   - Device EUI: `17c09b9ebf474ada`
   - Device Profile: `heltec-us915-otaa`

4. En la pestaña **Keys (OTAA)** ingresar:
   - App Key: `66450b8ad90d705d94025a4fb2866bd6`

### Sketch LoRaWAN con DHT11

> ⚠️ La Heltec WiFi LoRa 32 **V3** usa chip **SX1262** (no SX1276). Versiones anteriores V1/V2 usan SX1276. Usar `SX1276` en V3 causa error `-2`.

```cpp
#include <RadioLib.h>
#include <DHT.h>

#define DHTPIN 48
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);
SX1262 radio = new Module(8, 14, 12, 13);

uint64_t joinEUI =  0x4ACA057B56A0AB4C;
uint64_t devEUI  =  0x17C09B9EBF474ADA;
uint8_t appKey[] = { 0x66, 0x45, 0x0B, 0x8A, 0xD9, 0x0D, 0x70, 0x5D,
                     0x94, 0x02, 0x5A, 0x4F, 0xB2, 0x86, 0x6B, 0xD6 };
uint8_t nwkKey[] = { 0x66, 0x45, 0x0B, 0x8A, 0xD9, 0x0D, 0x70, 0x5D,
                     0x94, 0x02, 0x5A, 0x4F, 0xB2, 0x86, 0x6B, 0xD6 };

LoRaWANNode node(&radio, &US915, 2);

void setup() {
  Serial.begin(115200);
  dht.begin();
  Serial.println("Iniciando LoRaWAN + DHT11...");

  int state = radio.begin();
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("Error radio: "); Serial.println(state); while(true);
  }

  state = node.beginOTAA(joinEUI, devEUI, nwkKey, appKey);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.print("Error OTAA: "); Serial.println(state); while(true);
  }

  Serial.println("Haciendo join OTAA...");
  state = node.activateOTAA();
  if (state != RADIOLIB_LORAWAN_NEW_SESSION && state != RADIOLIB_LORAWAN_SESSION_RESTORED) {
    Serial.print("Join fallido: "); Serial.println(state); while(true);
  }
  Serial.println("¡Join exitoso!");
}

void loop() {
  float temp = dht.readTemperature();
  float hum  = dht.readHumidity();

  if (isnan(temp) || isnan(hum)) {
    Serial.println("Error leyendo DHT11");
    delay(5000);
    return;
  }

  // Empacar: temp y humedad como int16 × 10 (big-endian, 4 bytes total)
  uint8_t payload[4];
  int16_t t = (int16_t)(temp * 10);
  int16_t h = (int16_t)(hum  * 10);
  payload[0] = t >> 8;
  payload[1] = t & 0xFF;
  payload[2] = h >> 8;
  payload[3] = h & 0xFF;

  Serial.printf("Temp: %.1f°C  Hum: %.1f%%\n", temp, hum);

  int state = node.sendReceive(payload, sizeof(payload), 1);
  if (state == RADIOLIB_ERR_NONE || state == RADIOLIB_LORAWAN_DOWNLINK) {
    Serial.println("Datos enviados por LoRaWAN");
  } else {
    Serial.print("Error envío: "); Serial.println(state);
  }

  delay(30000);
}
```

### Verificación

En el Serial Monitor (115200 baud) debe aparecer:
```
Iniciando LoRaWAN + DHT11...
Haciendo join OTAA...
¡Join exitoso!
Temp: 25.2°C  Hum: 28.0%
Datos enviados por LoRaWAN
```

En ChirpStack → **Applications → iot-local-ipn → heltec-lora32-v3 → LoRaWAN Frames** deben verse los uplinks con FPort 1 y 4 bytes de payload.

---

## 7. Instalación de Node-RED y Dashboard

### Instalación

```bash
sudo apt install -y nodejs npm
sudo npm install -g --unsafe-perm node-red
```

### Instalar Dashboard 2.0

```bash
cd ~/.node-red
npm install @flowfuse/node-red-dashboard
```

### Configuración de red

Editar `~/.node-red/settings.js` y cambiar:

```js
uiHost: "0.0.0.0",
```

Esto permite acceder desde cualquier equipo de la red local.

### Iniciar Node-RED

```bash
node-red
```

O como servicio:
```bash
sudo systemctl enable nodered
sudo systemctl start nodered
```

Acceso:
```
Editor:    http://192.168.0.45:1880
Dashboard: http://192.168.0.45:1880/ui
```

### Flujo Node-RED para DHT11

El flujo consiste en tres nodos conectados en serie:

**1. Nodo mqtt in** — recibe datos de ChirpStack:
- Server: `192.168.0.45:1883`
- Topic: `application/+/device/+/event/up`
- Output: auto-detect (JSON)
- Name: `ChirpStack DHT11`

**2. Nodo function** — decodifica el payload base64:
- Name: `Decodificar DHT11`
- Outputs: **2**
- Código:

```javascript
var obj = msg.payload;
var b = Buffer.from(obj.data, 'base64');
var temp = ((b[0] << 8) | b[1]) / 10.0;
var hum  = ((b[2] << 8) | b[3]) / 10.0;
msg.payload = temp;
var msg2 = {payload: hum};
return [msg, msg2];
```

**3. Dos nodos gauge** (del @flowfuse/node-red-dashboard):
- Gauge Temperatura: conectado a salida 1, Group: `[IoT Local] Sensores`, Min: 0, Max: 50
- Gauge Humedad: conectado a salida 2, Group: `[IoT Local] Sensores`, Min: 0, Max: 100

> ⚠️ El nodo function debe tener **Outputs: 2** configurado, de lo contrario solo aparece una salida.

> ⚠️ Node-RED auto-parsea JSON del MQTT — no usar `JSON.parse()` en el function node.

---

## Solución de problemas

### Gateway "Never seen" en ChirpStack

**Causa más común:** Mismatch de topics MQTT entre Gateway Bridge y ChirpStack.

Verificar que el Gateway Bridge publica en `us915_0/...`:
```bash
docker compose logs chirpstack-gateway-bridge --tail 10
```

Si sigue publicando en `us915/...` (sin el `_0`), aplicar cambios con:
```bash
docker compose up -d --force-recreate chirpstack-gateway-bridge
```

> ⚠️ `docker compose restart` **no** recarga variables de entorno del `docker-compose.yml`. Usar siempre `--force-recreate` para aplicar cambios de configuración.

### Join fallido: -1116 (nonces descartados)

Ocurre cuando la Heltec tiene una sesión guardada que no coincide con el registro en ChirpStack. Solución:

1. En ChirpStack: eliminar el device y crearlo de nuevo (mismo EUI y App Key)
2. En Arduino IDE: subir el sketch de nuevo (esto hace un nuevo join OTAA)

### Error radio: -2

La placa está configurada como `SX1276` pero la Heltec V3 tiene `SX1262`. Cambiar:
```cpp
// MAL (V1/V2):
SX1276 radio = new Module(8, 14, 12, 13);

// BIEN (V3):
SX1262 radio = new Module(8, 14, 12, 13);
```

### Mosquitto no inicia como servicio

```bash
sudo mkdir -p /var/log/mosquitto /run/mosquitto /var/lib/mosquitto
sudo chown mosquitto /var/log/mosquitto /run/mosquitto /var/lib/mosquitto
sudo systemctl start mosquitto
```

### Verificar que llegan datos MQTT

```bash
mosquitto_sub -h 127.0.0.1 -p 1883 -t "application/#" -v
```

---

## Notas para instalación en el IPN

Cuando se mueva la instalación al IPN:

1. Solicitar una IP fija para el servidor (Raspberry Pi 5)
2. Actualizar `static ip_address` en `/etc/dhcpcd.conf` del Pi
3. Actualizar `server_address` en el archivo JSON de configuración del Sentrius
4. Re-subir la configuración al gateway via **LoRa → Advanced → Upload**
5. Actualizar el Server del nodo mqtt in en Node-RED con la nueva IP

No es necesario reinstalar ni reconfigurar ChirpStack — solo cambiar las IPs.

---

## Próximos pasos sugeridos

- [ ] Conectar múltiples nodos Heltec a la misma red
- [ ] Agregar sensores adicionales (CO2, presión, luz)
- [ ] Agregar gráfica histórica en Node-RED (nodo chart)
- [ ] Crear alertas por umbral de temperatura/humedad
- [ ] Crear aplicaciones IoT educativas con los datos recibidos

---

*Proyecto desarrollado para el Instituto Politécnico Nacional (IPN)*  
*Plataforma: Red LoRaWAN local sin internet para enseñanza de IoT*
