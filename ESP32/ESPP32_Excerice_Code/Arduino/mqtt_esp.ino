
////////////////////////////////////////////////////////////////////////////////
// Sending DHT11 sensor’s temperature and humidity data on Things Speak Cloud using MQTT protocol
////////////////////////////////////////////////////////////////////////////////////////////////

#include <WiFi.h>
#include <PubSubClient.h>
#include "DHT.h"
#define DHTPIN 32        // DHT11 connected to GPIO32
#define DHTTYPE DHT11   // DHT type
DHT dht(DHTPIN, DHTTYPE);
#define LED_PIN 2       // LED connected to GPIO2
// Wi-Fi Credentials
const char* ssid = "nature";      
const char* password = "nick123456"; 
 
// ThingSpeak MQTT details
const char* mqttServer = "mqtt3.thingspeak.com";
const int mqttPort = 1883;	//443 MQTT over WebSockets
const char* mqttUser = "XYZ";
const char* mqttPassword = "ABC";
const char* mqttClientId = "XYZ";
const char* topicPublish = "channels/Your channel_ID/publish";
const char* topicSubscribe = "channels/Your channel_ID/subscribe/fields/field1";
// Wi-Fi & MQTT Client
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastSendTime = 0; /*initialization for sending value on thingspeak every 15 sec */
void reconnectMQTT() 
{
  while (!client.connected()) 
   {
    Serial.print("Connecting to MQTT...");
    if (client.connect(mqttClientId, mqttUser, mqttPassword)) 
    {
      Serial.println("Connected!");
      client.subscribe(topicSubscribe);
    } 
    else 
    {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}
void callback(char* topic, byte* payload, unsigned int length) 
{
  Serial.print("Message received: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String message;
  
  for (int i = 0; i < length; i++) 
  {
    message += (char)payload[i];
  }
  Serial.println(message);
// Convert message to integer (1 or 0) and control LED
  int ledState = message.toInt();
  if (ledState == 1) 
  {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("LED ON");
  }
  else if (ledState == 0) 
  {
    digitalWrite(LED_PIN, LOW);
    Serial.println("LED OFF");
  } 
  else 
  {
    Serial.println("Invalid command received!");
  }
}
void loop() 
{
  if (!client.connected()) 
  {
    reconnectMQTT();
  }
  client.loop();	//To maintain the MQTT connection
  unsigned long currentMillis = millis();	
  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  Serial.print("Temp: "); Serial.print(temp); Serial.println(" °C");
  Serial.print("Humidity: "); Serial.print(hum); Serial.println(" %");
  delay(3000);
// Send data to ThingSpeak every 15 seconds  
  if (currentMillis - lastSendTime >= 15000) 
  {
    lastSendTime = currentMillis;
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
   if (!isnan(temp) && !isnan(hum)) 
   {
      String payload = "field1=" + String(temp) + "&field2=" + String(hum);
      client.publish(topicPublish, payload.c_str());
      Serial.println("Data sent to ThingSpeak!");
   }
  }
}
