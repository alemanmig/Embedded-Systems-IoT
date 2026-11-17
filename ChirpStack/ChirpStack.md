# ChirpStack desde cero

*Guía para el proyecto Gateway LoRaWAN con Raspberry Pi 5 — Fog vs Edge · 13 de noviembre de 2026*

## 1. Qué problema resuelve ChirpStack

ChirpStack es un servidor de red LoRaWAN de código abierto: hace el trabajo inteligente que el gateway no hace. El gateway no entiende los datos; solo recibe tramas de radio y las reenvía.

El servidor de red se encarga de:

- Saber qué dispositivos existen y si tienen permiso de estar en la red.
- Aceptar o rechazar cuando un nodo se une (el *join*).
- Eliminar duplicados cuando varios gateways escuchan la misma trama.
- Verificar la integridad de cada mensaje y descifrarlo.
- Decidir por qué gateway y cuándo mandar un downlink.
- Ajustar la velocidad de cada nodo (ADR).
- Entregar los datos a tu aplicación.

Cumple la misma función que The Things Network, pero instalado en tu propia infraestructura.

## 2. Dónde está en la cadena

ChirpStack se ubica entre el gateway y tu aplicación:

1. Sensor
2. Nodo (RP2040 + Wio-E5)
3. Aire: LoRa 915 MHz
4. Gateway (WM1302 en la Raspberry Pi 5)
5. **ChirpStack**
6. Tu aplicación (servicio de consenso)

## 3. Las piezas

Un sistema ChirpStack tiene cuatro grupos de piezas: los traductores del gateway, el broker MQTT, el propio ChirpStack y dos bases de datos.

| Pieza | Qué hace |
| --- | --- |
| Packet forwarder (`lora_pkt_fwd`) | Habla con el concentrador por SPI y saca las tramas por UDP al puerto 1700 |
| ChirpStack Gateway Bridge | Convierte el UDP de Semtech a MQTT, el idioma interno de ChirpStack. Alternativa moderna: Concentratord + MQTT Forwarder |
| Mosquitto (broker MQTT) | El "cartero" central: todos publican y se suscriben a *topics*, del gateway a ChirpStack y de ChirpStack a tus aplicaciones |
| ChirpStack v4 | Un solo programa con dos papeles. Servidor de red: joins, deduplicación, ADR y downlinks. Servidor de aplicación: descifra, decodifica y entrega los datos |
| PostgreSQL | Guarda la configuración: dispositivos, llaves, perfiles y usuarios |
| Redis | Guarda el estado rápido: sesiones activas, contadores de tramas y deduplicación |

## 4. Cómo se organiza dentro

En la interfaz web todo cuelga de un tenant, y cada dispositivo hereda su configuración de un device profile.

| Elemento | Qué es | Ejemplo |
| --- | --- | --- |
| Tenant | La organización | Laboratorio IoT |
| Gateway | Cada gateway registrado, identificado por su Gateway EUI | Raspberry Pi 5 + WM1302 |
| Device profile | Plantilla del tipo de dispositivo: región US915, versión LoRaWAN, clase A, OTAA o ABP, codec | Nodo RP2040 + Wio-E5 |
| Application | Agrupa dispositivos con un mismo propósito | Consenso 4 sensores |
| Device | Cada nodo, con su DevEUI, JoinEUI y AppKey | Nodo 1 a Nodo 4 |

## 5. Qué pasa cuando un nodo se une (OTAA)

En el join, nodo y servidor derivan las llaves de sesión sin que la AppKey viaje nunca por el aire.

1. El Wio-E5 envía un **Join Request** con su DevEUI y su JoinEUI, firmado con la AppKey.
2. ChirpStack busca ese DevEUI en PostgreSQL y verifica la firma.
3. Si todo está bien, responde con un **Join Accept**. Ambos lados derivan las llaves de sesión: **NwkSKey** (red) y **AppSKey** (aplicación). El nodo recibe además una dirección corta, el **DevAddr**.
4. La AppKey nunca se transmite: buen punto de discusión para la clase de seguridad.

## 6. Qué pasa con cada dato (uplink)

Cada uplink sale cifrado del nodo y llega a tu aplicación como JSON legible, en seis pasos.

1. El nodo cifra el payload con la AppSKey y transmite.
2. El gateway lo recibe y lo publica en MQTT, en un topic tipo `us915_0/gateway/<EUI>/event/up`.
3. ChirpStack elimina duplicados, verifica el MIC con la NwkSKey, revisa el contador de tramas (contra *replay attacks*) y descifra con la AppSKey.
4. El **codec**, una función JavaScript en el device profile, convierte los bytes en JSON. Por ejemplo, de `0x01 0x2C` a `{"temp": 30.0}`.
5. ChirpStack publica el resultado en `application/<id>/device/<DevEUI>/event/up`.
6. El servicio de consenso se suscribe a ese topic y recibe los datos limpios, junto con los metadatos `rxInfo`: RSSI, SNR y qué gateway lo recibió.

## 7. Integraciones

Además de MQTT, ChirpStack puede mandar los datos por HTTP (webhooks) o directo a InfluxDB y otros servicios. Para los alumnos, MQTT es la integración más clara.

## 8. En el proyecto fog vs. edge

Las mismas piezas corren en el servidor actual (fog) o dentro de la Raspberry Pi 5 (edge).

- **Fase 1 (Fog):** todo esto ya corre en el servidor ChirpStack actual. Solo falta agregar el codec y el servicio de consenso.
- **Fase 3 (Edge):** se levantan exactamente las mismas piezas dentro de la Pi 5 con Docker Compose; el repositorio `chirpstack-docker` trae casi todo listo. La interfaz web queda en `http://<ip-de-la-pi>:8080`. El usuario inicial es admin/admin, y lo primero es cambiarlo.
