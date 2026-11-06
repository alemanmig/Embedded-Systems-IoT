#include <Arduino_FreeRTOS.h>  //Aplicacion Real Time => Real Time Kernel 

// Nombres simbolicos que representan los pines fisicos
#define RED    6
#define YELLOW 7
#define BLUE   8

typedef int TaskProfiler;  //Nuevo tipo de datos llamado TaskProfiler

TaskProfiler RedLEDProfiler;
TaskProfiler YellowLEDProfiler;
TaskProfiler BlueLEDProfiler;

void setup()   //setup function
{
  Serial.begin(9600);
  xTaskCreate(                     //xTaskCreate Crear una tarea
    redLedControllerTask,          //
    "Red LED Task",
    100,
    NULL,
    1,  //Prioridad
    NULL
  );
  xTaskCreate(
    blueLedControllerTask, // Pasamos la tarea aqui  
    "Blue LED Task",       // Nombre descriptivo para el debuging
    100,                   // Cada Task requiere un stack (pila), entre 100 - 128 Arduino no tiene mucha memoria
    NULL,                  // No tenemos nada que pasar 
    1,  //Prioridad        // Prioridad 
    NULL                   // 
  );
  xTaskCreate(
    yellowLedControllerTask,
    "Yelow LED Task",
    100,
    NULL,
    1,  //Prioridad
    NULL
  );
}

void redLedControllerTask(void *pvParameters)   // Ponemos el contenido en las Task y es de tipo void no retiene nada
{                                                
  pinMode(RED,OUTPUT);

  while(1)          // LOOP infinito
  {
   Serial.println("This is RED");    // Imprimimos en el Monitor serial
  }
}

void blueLedControllerTask(void *pvParameters)
{
  pinMode(BLUE,OUTPUT);

  while(1)
  {
   Serial.println("This is BLUE");
  }
}

void yellowLedControllerTask(void *pvParameters)
{
  pinMode(YELLOW,OUTPUT);

  while(1)
  {
   Serial.println("This is YELLOW");
  }
}

void loop()
{}