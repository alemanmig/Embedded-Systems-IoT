# FreeRTOS en Sistemas Embebidos

Notas y ejemplos para aprender **RTOS** con **FreeRTOS**, empezando por un ATmega328 (Arduino UNO/Nano) con la librería `Arduino_FreeRTOS`.

---

## Contenido

1. [¿Qué es un RTOS?](#1-qué-es-un-rtos)
2. [Diferencias con Linux o Windows](#2-diferencias-con-linux-o-windows)
3. [¿Qué es FreeRTOS?](#3-qué-es-freertos)
4. [Características de FreeRTOS](#4-características-de-freertos)
5. [Archivos del kernel](#5-archivos-del-kernel)
6. [Convención de nombres](#6-convención-de-nombres)
7. [¿Un ATmega328 realmente "corre un sistema operativo"?](#7-un-atmega328-realmente-corre-un-sistema-operativo)
8. [Del super-loop a tasks](#8-del-super-loop-a-tasks)
9. [Siguientes pasos](#9-siguientes-pasos)

---

## 1. ¿Qué es un RTOS?

Un **RTOS (Real-Time Operating System)** es un sistema operativo cuyo objetivo principal es el **determinismo**: garantizar que una tarea se ejecute dentro de un tiempo acotado y predecible. No busca ser rápido en promedio, sino ser **predecible en el peor caso**.

- **Hard real-time:** perder un deadline es una falla del sistema (airbag, control de motor, marcapasos).
- **Soft real-time:** perder un deadline degrada la calidad, pero no es catastrófico (audio, video).

En la práctica, en microcontroladores un RTOS es sobre todo un **kernel**: un scheduler más primitivas de sincronización y comunicación. El kernel está en el centro, decidiendo qué hilo (task) ocupa la CPU en cada momento:

```
                 ┌──────────┐
                 │ Thread 1 │
                 └────▲─────┘
                      │
 ┌──────────┐   ┌─────┴─────┐   ┌──────────┐
 │ Thread 2 ◄───┤  Kernel   ├───► Thread 5 │
 └──────────┘   └──┬─────┬──┘   └──────────┘
                   │     │
          ┌────────▼─┐ ┌─▼────────┐
          │ Thread 3 │ │ Thread 4 │
          └──────────┘ └──────────┘
```

---

## 2. Diferencias con Linux o Windows

| Aspecto | RTOS (FreeRTOS) | GPOS (Linux / Windows) |
|---|---|---|
| Objetivo | Determinismo, latencia acotada | Throughput, equidad, experiencia de usuario |
| Scheduler | Preemptivo por **prioridad fija**: siempre corre la tarea lista de mayor prioridad | Políticas "justas" (CFS en Linux) que reparten CPU |
| Memoria | Sin MMU, todo comparte un espacio de direcciones | Memoria virtual, procesos aislados |
| Tamaño | KB (kernel de ~5–10 KB de flash) | MB a GB |
| Estructura | Kernel y aplicación se **compilan juntos en un solo binario** | El kernel carga y ejecuta programas independientes |
| Servicios | Tasks, colas, semáforos, timers | Filesystem, red, drivers, shell, usuarios, etc. |
| Arranque | Milisegundos | Segundos |

La idea central: en Linux tu programa es un **proceso** que el SO carga. En FreeRTOS **no hay procesos**, solo tasks (hilos) dentro de una misma aplicación. FreeRTOS es más una **biblioteca de scheduling** que un SO en el sentido de Windows.

---

## 3. ¿Qué es FreeRTOS?

Es un kernel de tiempo real open source (licencia MIT), escrito en C, portado a más de 40 arquitecturas (AVR, ARM Cortex-M, RISC-V, ESP32, etc.). Lo mantiene AWS desde 2017. Su ventaja es que es pequeño, simple de leer y muy usado en la industria.

### Variantes

- **OpenRTOS:** el mismo código de FreeRTOS, con licencia comercial y soporte de WITTENSTEIN. Sirve para empresas que necesitan garantías legales o de soporte.
- **SafeRTOS:** una reescritura del kernel hecha para certificación de seguridad funcional (IEC 61508, ISO 26262, IEC 62304). Se usa en automotriz, médico e industrial.

---

## 4. Características de FreeRTOS

- **Preemptive scheduling:** una tarea de mayor prioridad que pasa a "lista" desplaza de inmediato a la que corre.
- **Inter-thread communication:** queues, stream/message buffers, task notifications.
- **Thread synchronization:** semáforos binarios y contadores, mutex (con herencia de prioridad), event groups.
- **Hooks:** callbacks que tú defines:
  - `vApplicationIdleHook`
  - `vApplicationTickHook`
  - `vApplicationStackOverflowHook`
  - `vApplicationMallocFailedHook`
- **Trace recording:** macros `trace...` para herramientas como Tracealyzer.
- **Run-time statistics:** cuánto tiempo de CPU consumió cada tarea.
- **Tick-less** (no "thick-less"): en modo de bajo consumo, el kernel suprime la interrupción periódica del tick mientras no hay trabajo y duerme el micro. Es clave en IoT con batería.

---

## 5. Archivos del kernel

| Archivo | Rol |
|---|---|
| `tasks.c` | Scheduler y gestión de tareas (obligatorio) |
| `list.c` | Listas enlazadas internas del kernel (obligatorio) |
| `queue.c` | Colas, semáforos y mutex (prácticamente siempre) |
| `timers.c` | Software timers (opcional) |
| `event_groups.c` | Event groups (opcional) |
| `stream_buffer.c` | Stream y message buffers (opcional) |
| `croutine.c` | Co-rutinas (legado, casi no se usa) |
| `port.c` + `portmacro.h` | **Dependientes de la arquitectura**: cambio de contexto y tick |
| `heap_1..5.c` | Esquemas de asignación de memoria (eliges uno) |

> **Nota:** `FreeRTOSConfig.h` **no** es un archivo común del kernel: lo escribe cada aplicación. Ahí configuras `configUSE_PREEMPTION`, `configTICK_RATE_HZ`, `configTOTAL_HEAP_SIZE`, etc.

---

## 6. Convención de nombres

### 6.1 Prefijos de variables

| Prefijo | Tipo |
|---|---|
| `c` | `char` / `int8_t` |
| `s` | `int16_t` (short) |
| `l` | `int32_t` (long) |
| `x` | `BaseType_t` y cualquier tipo no estándar: structs, handles, `TickType_t` |
| `u` | unsigned, se combina: `uc` = `uint8_t`, `us` = `uint16_t`, `ul` = `uint32_t`, `ux` = `UBaseType_t` |
| `p` | puntero, se combina: `pc` = `char*`, `pv` = `void*`, `px` = puntero a tipo no estándar |
| `e` | enum |

> **Nota:** `BaseType_t` usa `x`, no `b`. La `b` no forma parte del estándar de FreeRTOS.

### 6.2 Prefijos de funciones

Los nombres de funciones llevan dos prefijos:

1. **Tipo de retorno** de la función.
2. **Archivo** donde está definida.

| Función | Retorna | Definida en |
|---|---|---|
| `vTaskPrioritySet()` | `void` | `tasks.c` |
| `xQueueReceive()` | `BaseType_t` | `queue.c` |
| `pvTimerGetTimerID()` | `void *` | `timers.c` |
| `uxTaskPriorityGet()` | `UBaseType_t` | `tasks.c` |
| `ulTaskNotifyTake()` | `uint32_t` | `tasks.c` |
| `pcTaskGetName()` | `char *` | `tasks.c` |
| `prvIdleTask()` | `prv` = **privada** (`static`) | `tasks.c` |

Ejemplos:

- `vTaskPrioritySet()` retorna `void` y está definida en `tasks.c`.
- `xQueueReceive()` retorna `BaseType_t` y está definida en `queue.c`.
- `pvTimerGetTimerID()` retorna un puntero a `void` y está definida en `timers.c`.

> **Notas:**
> - El ejemplo correcto es **`xQueueReceive()`**, no `cQueueReceive()`, porque `BaseType_t` lleva `x`.
> - El archivo es **`tasks.c`** (en plural); su header es `task.h`.

### 6.3 Nombres de macros

La mayoría de las macros están escritas en mayúsculas:

- El **nombre** de la macro va en **mayúsculas**.
- El **prefijo** va en **minúsculas**.
- El prefijo indica el **archivo** donde está definida la macro.

Ejemplo: `portMAX_DELAY`

- Prefijo: `port`
- Macro: `MAX_DELAY`
- Ubicada en: `portable.h`

| Macro | Prefijo | Archivo |
|---|---|---|
| `portMAX_DELAY` | `port` | `portable.h` / `portmacro.h` |
| `taskENTER_CRITICAL()` | `task` | `task.h` |
| `pdTRUE` | `pd` | `projdefs.h` |
| `configUSE_PREEMPTION` | `config` | `FreeRTOSConfig.h` |
| `errQUEUE_FULL` | `err` | `projdefs.h` |
| `queueSEND_TO_BACK` | `queue` | `queue.h` |

### 6.4 Valores comunes

| Macro | Valor |
|---|---|
| `pdTRUE` | 1 |
| `pdFALSE` | 0 |
| `pdPASS` | 1 |
| `pdFAIL` | 0 |

> **Tip:** `pdMS_TO_TICKS(ms)` (de `projdefs.h`) convierte milisegundos a ticks. Lo vas a usar todo el tiempo.

---

## 7. ¿Un ATmega328 realmente "corre un sistema operativo"?

Sí y no. **No** corre un SO como Linux: no hay procesos, MMU, filesystem ni carga de programas. **Sí** corre un **kernel multitarea real**. Esto es lo que pasa físicamente:

1. **Cada task tiene su propia pila** en la RAM (de solo 2 KB en el 328).
2. Un **timer genera una interrupción periódica**, el *tick*. En la librería `Arduino_FreeRTOS` (de feilipu) se usa el **Watchdog Timer**, con un tick por defecto de unos **15 ms**.
3. En cada tick, la ISR del kernel:
   - **guarda el contexto** de la tarea actual (los 32 registros, SREG y PC) en *su* pila,
   - el scheduler elige la siguiente tarea lista de mayor prioridad,
   - **cambia el stack pointer** a la pila de esa tarea y restaura sus registros,
   - al hacer `reti`, la CPU "regresa" a otra tarea.

El micro sigue ejecutando una instrucción a la vez. La concurrencia es una **ilusión creada por los cambios de contexto**. Todo, kernel y tus tasks, se compila en **un solo `.hex`**, igual que un sketch normal.

### Detalles específicos de `Arduino_FreeRTOS`

- **No llamas `vTaskStartScheduler()`**: la librería lo hace automáticamente después de `setup()`.
- **`loop()` se ejecuta dentro de la Idle Task** (como idle hook), así que nunca debes bloquear ni usar `delay()` largos ahí.

---

## 8. Del super-loop a tasks

### 8.1 Versión Arduino (super-loop)

```cpp
#define RED     6
#define YELLOW  7
#define GREEN   8

void setup() {
  pinMode(RED,OUTPUT);
  pinMode(YELLOW,OUTPUT);
  pinMode(GREEN,OUTPUT);
}

void loop() {
  digitalWrite(RED,digitalRead(RED)^1);
  digitalWrite(YELLOW,digitalRead(YELLOW)^1);
  digitalWrite(GREEN,digitalRead(GREEN)^1);
  delay(50);
}
```

Un solo hilo, los tres LEDs **acoplados**: cambian juntos cada 50 ms. Si quieres que cada uno tenga su propio periodo, tienes que hacer malabares con `millis()`. Este es el problema que resuelve un RTOS.

### 8.2 Primera versión con FreeRTOS: compila, pero tiene un error de diseño

```cpp
#include <Arduino_FreeRTOS.h>

#define RED     6
#define YELLOW  7
#define BLUE    8

void setup() {

// hilos tasks
   xTaskCreate(redLedControllerTask,"RED LED Task",128,NULL,1,NULL);
   xTaskCreate(blueLedControllerTask,"BLUE LED Task",128,NULL,1,NULL);
   xTaskCreate(yellowLedControllerTask,"YELLOW LED Task",128,NULL,1,NULL);


}

// Task definition
void redLedControllerTask(void *pvParameters)
{
  pinMode(RED,OUTPUT);

  while(1)
  {
     digitalWrite(RED,digitalRead(RED)^1);

  }
}

void  blueLedControllerTask(void *pvParameters)
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
void loop() {}
```

Cada task hace `while(1)` **sin bloquearse nunca**. Esto provoca:

1. **Las tres tareas tienen prioridad 1 y siempre están "Ready"**, así que el scheduler hace *round-robin* por time-slicing: cada una corre unos 15 ms y luego cede.
2. Dentro de esos 15 ms, el LED se conmuta **miles de veces**. Lo que ves no es parpadeo, sino un LED encendido "a media intensidad" (PWM accidental de ~50 %).
3. La **Idle Task nunca corre**, porque siempre hay alguien listo con prioridad mayor. Eso implica que `loop()` no se ejecuta, no hay limpieza de memoria y no hay bajo consumo.
4. Se desperdicia el 100 % de la CPU en *busy-waiting*.

> **Regla de oro del RTOS:** una tarea debe **bloquearse** (con `vTaskDelay`, esperando una cola o un semáforo, etc.) para ceder la CPU. Una tarea que nunca se bloquea "mata de hambre" a las de prioridad igual o menor.

### 8.3 Versión corregida (y que aprovecha el RTOS)

```cpp
#include <Arduino_FreeRTOS.h>

#define RED     6
#define YELLOW  7
#define BLUE    8

void redLedControllerTask(void *pvParameters);
void yellowLedControllerTask(void *pvParameters);
void blueLedControllerTask(void *pvParameters);

void setup() {
  // Stack en el port AVR: StackType_t = uint8_t, así que 128 = 128 bytes
  xTaskCreate(redLedControllerTask,    "RED",    128, NULL, 1, NULL);
  xTaskCreate(yellowLedControllerTask, "YELLOW", 128, NULL, 1, NULL);
  xTaskCreate(blueLedControllerTask,   "BLUE",   128, NULL, 1, NULL);
  // El scheduler arranca solo al terminar setup()
}

void redLedControllerTask(void *pvParameters) {
  pinMode(RED, OUTPUT);
  for (;;) {
    digitalWrite(RED, digitalRead(RED) ^ 1);
    vTaskDelay(pdMS_TO_TICKS(100));   // se bloquea y cede la CPU
  }
}

void yellowLedControllerTask(void *pvParameters) {
  pinMode(YELLOW, OUTPUT);
  for (;;) {
    digitalWrite(YELLOW, digitalRead(YELLOW) ^ 1);
    vTaskDelay(pdMS_TO_TICKS(300));
  }
}

void blueLedControllerTask(void *pvParameters) {
  pinMode(BLUE, OUTPUT);
  for (;;) {
    digitalWrite(BLUE, digitalRead(BLUE) ^ 1);
    vTaskDelay(pdMS_TO_TICKS(700));
  }
}

void loop() {
  // Corre en la Idle Task: no bloquear aquí
}
```

Ahora cada LED tiene **su propio periodo, independiente**, sin una sola línea de `millis()`. Esa es la ganancia real: **separar responsabilidades en tareas**. Y mientras las tres están bloqueadas, corre la Idle Task.

### 8.4 Precauciones en el ATmega328

- **Resolución del tick:** con un tick de unos 15 ms, `pdMS_TO_TICKS(50)` da 3 ticks, o sea unos 45 ms. En el 328 con WDT no hay precisión fina de milisegundos.
- **RAM:** 3 tareas de 128 B, más sus TCB, más la Idle Task y el heap ya consumen buena parte de los 2 KB. Si agregas tareas y el micro se reinicia o se cuelga, sospecha primero de un *stack overflow*. Para diagnosticarlo existen:
  - `uxTaskGetStackHighWaterMark()`
  - `configCHECK_FOR_STACK_OVERFLOW`

---

