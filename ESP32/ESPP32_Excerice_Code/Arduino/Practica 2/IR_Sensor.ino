///////////////////////////////////////////////////////////////////////
// IR Sensor Object Detection Using ESP32 Dev Kit
// File. IR_Sensor.ino
////////////////////////////////////////////////////////////////////////

#define IR_SENSOR_PIN 12	// IR sensor output pin connected to GPIO12
#define BUZZER_PIN 13		// Buzzer connected to GPIO13
#define LED_PIN 2			// Onboard LED of ESP32 (GPIO2)

void setup() 
{
	pinMode(IR_SENSOR_PIN, INPUT_PULLUP);
	pinMode(BUZZER_PIN, OUTPUT);
	pinMode(LED_PIN, OUTPUT);
	digitalWrite(BUZZER_PIN, LOW);
	digitalWrite(LED_PIN, LOW);
	Serial.begin(115200); // Start Serial Monitor at 115200 baud
}
void loop() 
{
int sensorState = digitalRead(IR_SENSOR_PIN);	//Read sensor state
	if (sensorState == LOW)					//If object is detected
	{
	Serial.println("Object Detected");
	digitalWrite(LED_PIN, HIGH);			//Turn on onboard LED
	digitalWrite(BUZZER_PIN, HIGH);		//Turn on buzzer
	delay(500);						//Keep buzzer ON for 500ms
	digitalWrite(BUZZER_PIN, LOW);		//Turn off buzzer
	} 
	else 
	{
	Serial.println("No Object Detected");
	digitalWrite(LED_PIN, LOW);			//Turn off onboard LED
	}
	delay(500);	//Small delay to stabilize readings and avoid serial flooding
}
