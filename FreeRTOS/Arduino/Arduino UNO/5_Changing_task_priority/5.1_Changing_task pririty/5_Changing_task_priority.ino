/*
 * Sketch 05 - Changing_task_priority
 * Arduino UNO + Arduino_FreeRTOS 
 *
 * Objetivo: VER el efecto de vTaskPrioritySet() en los LEDs.
 *
 * Comportamiento esperado:
 *   0-4 s : los 3 LEDs parpadean (prioridad 1, comparten la CPU por time slicing)
 *   4-8 s : amarillo sube a prioridad 2 -> rojo y azul se congelan
 *   8-12 s: amarillo baja a prioridad 1 -> los 3 parpadean otra vez
 *   ... y se repite el ciclo. Monitor serie a 9600 baudios.
 */

#include <Arduino_FreeRTOS.h>

#define RED    6
#define YELLOW 7
#define BLUE   8

#define STACK_SIZE   128   // En el port AVR la pila se mide en BYTES
#define BLINK_MS     200   // Medio periodo de parpadeo
#define TOGGLES_CAMBIO 20  // 20 x 200 ms = 4 s entre cambios de prioridad

TaskHandle_t red_Handle    = NULL;
TaskHandle_t blue_Handle   = NULL;
TaskHandle_t yellow_Handle = NULL;

// Espera activa: ocupa la CPU SIN ceder el control al planificador.
// millis() sigue funcionando porque el tick de FreeRTOS usa el Watchdog Timer,
// no el Timer0.
static void busyWait(uint32_t ms)
{
  uint32_t t0 = millis();
  while (millis() - t0 < ms) {
    // nada: solo consumir CPU
  }
}

void redLedControllerTask(void *pvParameters)
{
  (void) pvParameters;
  for (;;) {
    digitalWrite(RED, !digitalRead(RED));
    busyWait(BLINK_MS);
  }
}

void blueLedControllerTask(void *pvParameters)
{
  (void) pvParameters;
  for (;;) {
    digitalWrite(BLUE, !digitalRead(BLUE));
    busyWait(BLINK_MS);
  }
}

void yellowLedControllerTask(void *pvParameters)
{
  (void) pvParameters;
  uint8_t toggles = 0;

  for (;;) {
    digitalWrite(YELLOW, !digitalRead(YELLOW));
    busyWait(BLINK_MS);

    if (++toggles >= TOGGLES_CAMBIO) {
      toggles = 0;

      UBaseType_t actual = uxTaskPriorityGet(NULL);   // NULL = esta misma tarea
      UBaseType_t nueva  = (actual == 1) ? 2 : 1;

      Serial.print(F("Amarillo: prioridad "));
      Serial.print(actual);
      Serial.print(F(" -> "));
      Serial.println(nueva);
      Serial.flush();

      vTaskPrioritySet(NULL, nueva);  // se cambia UNA vez, no en cada vuelta
    }
  }
}

void setup()
{
  Serial.begin(9600);

  pinMode(RED, OUTPUT);
  pinMode(YELLOW, OUTPUT);
  pinMode(BLUE, OUTPUT);

  if (xTaskCreate(redLedControllerTask, "RED", STACK_SIZE, NULL, 1, &red_Handle) != pdPASS)
    Serial.println(F("Error: no se creo la tarea ROJA"));

  if (xTaskCreate(blueLedControllerTask, "BLUE", STACK_SIZE, NULL, 1, &blue_Handle) != pdPASS)
    Serial.println(F("Error: no se creo la tarea AZUL"));

  if (xTaskCreate(yellowLedControllerTask, "YELLOW", STACK_SIZE, NULL, 1, &yellow_Handle) != pdPASS)
    Serial.println(F("Error: no se creo la tarea AMARILLA"));

  Serial.println(F("Tareas creadas. Todas con prioridad 1."));
  // En esta librería el planificador arranca solo al terminar setup().
}

void loop()
{
  // loop() corre dentro de la tarea Idle (prioridad 0).
  // Como las tareas de arriba nunca se bloquean, loop() casi no se ejecutará:
  // eso también es una consecuencia de las prioridades.
}
