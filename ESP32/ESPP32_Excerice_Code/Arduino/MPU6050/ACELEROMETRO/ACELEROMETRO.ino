#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Crear una instancia del sensor
Adafruit_MPU6050 mpu;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  // Inicializar el MPU6050
  if (!mpu.begin()) {
    Serial.println("No se pudo encontrar un MPU6050. Verifique la conexión.");
    while (1);
  }

  Serial.println("MPU6050 encontrado");
}

void loop() {
  sensors_event_t a;
  mpu.getAccelerometerSensor()->getEvent(&a);

  // Imprimir los datos para el Serial Plotter
  Serial.print("Aceleracion_X:");
  Serial.print(a.acceleration.x);
  Serial.print("\tAceleracion_Y:");
  Serial.print(a.acceleration.y);
  Serial.print("\tAceleracion_Z:");
  Serial.println(a.acceleration.z);


  delay(100); // Retardo para actualizar los datos
}
