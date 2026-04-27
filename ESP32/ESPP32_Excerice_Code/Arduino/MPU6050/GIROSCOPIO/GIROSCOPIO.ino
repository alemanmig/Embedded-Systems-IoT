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
  sensors_event_t g;
  mpu.getGyroSensor()->getEvent(&g);

  // Imprimir los datos para el Serial Plotter
  Serial.print("Giroscopio_X:");
  Serial.print(g.gyro.x);
  Serial.print("\tGiroscopio_Y:");
  Serial.print(g.gyro.y);
  Serial.print("\tGiroscopio_Z:");
  Serial.println(g.gyro.z);

  delay(100); // Retardo para actualizar los datos
}
