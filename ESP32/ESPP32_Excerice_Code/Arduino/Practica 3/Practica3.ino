// Practica3 – 3: ESP32 STA Mode | Wireless Device Control 

#include <WiFi.h>
const char* ssid = "test";      	// Your WiFi Name
const char* password = "12345678";  // Your WiFi Password
WiFiServer server(80);        		// Start server on port 80
WiFiClient client;
String request;			//declare a string variable
#define LED_PIN 2         			// GPIO02 for LED
void setup()
{
	Serial.begin(9600);
	pinMode(LED_PIN, OUTPUT);
	digitalWrite(LED_PIN, LOW);     	// Ensure LED is OFF at start
	WiFi.begin(ssid, password);     	// Connect to Wi-Fi
	Serial.print("Connecting to WiFi...");
	while (WiFi.status() != WL_CONNECTED) 
	{
	delay(500);
	Serial.print(".");
	}
	Serial.println("\nConnected to WiFi!");
	Serial.print("ESP32 IP Address: ");
	Serial.println(WiFi.localIP());  // Print ESP32 IP
	server.begin(); // Start Web Server
}
void loop() 
{	client = server.available();
	if (client)
	{
	String request = client.readStringUntil('\n');
	request.trim();
	if (request.indexOf("GET /favicon.ico") != -1)
	{
	client.stop();
	return; 
	}
Serial.println(request);
	if(request == "GET /ledon HTTP/1.1")
	{
	digitalWrite(LED_PIN, HIGH);
	}
	if(request == "GET /ledoff HTTP/1.1")
	{
	digitalWrite(LED_PIN, LOW);
	}
// Send Response with LED Control Buttons
	client.println("HTTP/1.1 200 OK");
	client.println("Content-Type: text/html");
	client.println("Connection: close");
	client.println();		//end of the HTML Header
	client.println("<!DOCTYPE html><html><head><title>ESP32 LED Control</title>");
	client.println("<meta name='viewport' content='width=device-width, initial-scale=1'>");
	client.println("<style>button{padding:10px 20px;font-size:20px;}</style>");
	client.println("</head><body style='text-align:center;'>");
	client.println("<h1>ESP32 LED Control</h1>");
	client.println("<p><a href='/ledon'><button>LED ON</button></a></p>");
	client.println("<p><a href='/ledoff'><button>LED OFF</button></a></p>");
	client.println("</body></html>");
	client.stop(); // Close connection
	Serial.println("Client Disconnected.");
	}	
}
