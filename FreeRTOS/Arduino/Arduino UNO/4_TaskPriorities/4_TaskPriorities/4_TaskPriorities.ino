#include <Arduino_FreeRTOS.h> 

#define RED    6
#define YELLOW 7
#define BLUE   8

typedef int TaskProfiler;  

TaskProfiler RedLEDProfiler;
TaskProfiler YellowLEDProfiler;
TaskProfiler BlueLEDProfiler;

void setup() {
  xTaskCreate(redLedControllerTask,"RED LED Task",100,NULL,3,NULL);
  xTaskCreate(blueLedControllerTask,"BLUE LED Task",100,NULL,2,NULL);
  xTaskCreate(yellowLedControllerTask,"YELLOW LED Task",100,NULL,2,NULL);

}

void redLedControllerTask(void *pvParametres)
{
  pinMode(RED,OUTPUT);
  while(1)
  {
   digitalWrite(RED,digitalRead(RED)^1);
  }
}

void blueLedControllerTask(void *pvParameters)
{
  pinMode(BLUE,OUTPUT);
  while(1)
  {
   digitalWrite(BLUE,digitalRead(BLUE)^1);
  }
}

void yellowLedControllerTask(void *pvParameters)
{
  pinMode(YELLOW,OUTPUT);
  while(1)
  {
   digitalWrite(YELLOW,digitalRead(YELLOW)^1);
  }
}

void loop() {
}
