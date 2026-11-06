#include <Arduino_FreeRTOS.h> 

#define RED    6
#define YELLOW 7
#define BLUE   8

typedef int TaskProfiler;  

TaskProfiler RedLEDProfiler;
TaskProfiler YellowLEDProfiler;
TaskProfiler BlueLEDProfiler;

TaskHandle_t blue_Handle, red_Handle, yellow_Handle;  // nueva variable Task Handle

void setup() {
  xTaskCreate(redLedControllerTask,"RED LED Task",100,NULL,1,&red_Handle);
  xTaskCreate(blueLedControllerTask,"BLUE LED Task",100,NULL,1,&blue_Handle);
  xTaskCreate(yellowLedControllerTask,"YELLOW LED Task",100,NULL,1,&yellow_Handle);

}

void redLedControllerTask(void *pvParametres)
{
  pinMode(RED,OUTPUT);
  while(1)
  {
   digitalWrite(RED,digitalRead(RED)^1);
   vTaskDelay(pdMS_TO_TICKS(100));
   //delay(50);
  }
}

void blueLedControllerTask(void *pvParameters)
{
  pinMode(BLUE,OUTPUT);
  while(1)
  {
   digitalWrite(BLUE,digitalRead(BLUE)^1);
   vTaskDelay(pdMS_TO_TICKS(100));
   //delay(50);
  }
}

void yellowLedControllerTask(void *pvParameters)
{
  pinMode(YELLOW,OUTPUT);
  while(1)
  {
   digitalWrite(YELLOW,digitalRead(YELLOW)^1);
   vTaskPrioritySet(yellow_Handle,2);
   vTaskDelay(pdMS_TO_TICKS(100));
   //delay(50);
  }
}

void loop() {
}
