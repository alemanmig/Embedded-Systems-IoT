#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

#if !defined(CONFIG_BT_SPP_ENABLED)
#error Serial Bluetooth not available or not enabled. It is only available for the ESP32 chip.
#endif

BluetoothSerial SerialBT;

// Crear una instancia del sensor
Adafruit_MPU6050 mpu;

void setup() {
  
  SerialBT.begin("ESP32_Device");
  Wire.begin();

  // Inicializar el MPU6050
  if (!mpu.begin()) {
    //SerialBT.println("No se pudo encontrar un MPU6050. Verifique la conexión.");
    while (1);
  }

  //SerialBT.println("MPU6050 encontrado");
}

void loop() {
  
  sensors_event_t a;
  mpu.getAccelerometerSensor()->getEvent(&a);


  // Enviar valores a Python
  SerialBT.println("E");
  SerialBT.println(a.acceleration.x);
  SerialBT.println(a.acceleration.y);
  SerialBT.println(a.acceleration.z);


  delay(100); // Retardo para actualizar los datos
}
