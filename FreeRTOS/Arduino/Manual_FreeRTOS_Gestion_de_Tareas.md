# Manual FreeRTOS: Gestión de Tareas

4 de noviembre de 2026

## 1. Introducción: ¿qué es una tarea?

En FreeRTOS, una **tarea (task)** es un programa independiente que corre como si tuviera el procesador para ella sola. Cada tarea tiene su propia pila (stack), su propia prioridad y su propio estado.

En un programa "bare metal" clásico (el `loop()` de Arduino) todo vive en un solo ciclo, y una función lenta retrasa a todas las demás. Con FreeRTOS divides la aplicación en varias tareas y el **planificador (scheduler)** decide cuál ejecuta en cada momento, según su prioridad y su estado.

Este manual cubre tres piezas básicas de la gestión de tareas:

1. Cómo se escribe una tarea: una función en C con una firma fija.
2. En qué estados puede estar una tarea: Running y Not Running.
3. Cómo se crea una tarea: la función `xTaskCreate()`.

Los ejemplos usan la librería **Arduino_FreeRTOS** sobre ATmega328 (Arduino UNO), pero los conceptos son los mismos en cualquier microcontrolador.

## 2. La tarea como función en C

Toda tarea se implementa como una función de C con esta firma exacta:

```c
void ATaskFunction( void *pvParameters );
```

| Parte | Significado |
| --- | --- |
| `void` (retorno) | La tarea **no regresa ningún valor**. De hecho, nunca debe llegar a un `return`. |
| `ATaskFunction` | Nombre libre; es el que pasarás a `xTaskCreate()`. |
| `void *pvParameters` | Puntero genérico. Permite pasar **cualquier dato** a la tarea: un entero, una cadena, una estructura. Dentro de la tarea se hace *cast* al tipo real. |

El prefijo `pv` sigue la convención de nombres de FreeRTOS: `p` = puntero, `v` = void. Verás lo mismo en `x` (tipo `BaseType_t`), `ux` (unsigned), `pc` (puntero a char) y `us` (unsigned short).

### Estructura típica de una tarea

```c
void vTareaEjemplo( void *pvParameters )
{
    /* 1. Inicialización: se ejecuta una sola vez */
    int contador = 0;   /* variable local: cada instancia tiene la suya */

    /* 2. Bucle infinito: el cuerpo de la tarea */
    for( ;; )
    {
        contador++;
        /* ... trabajo de la tarea ... */
        vTaskDelay( 500 / portTICK_PERIOD_MS );  /* cede el CPU 500 ms */
    }

    /* 3. Nunca se llega aquí. Si la tarea debe terminar,
          se borra a sí misma: */
    vTaskDelete( NULL );
}
```

### Reglas clave

- **Bucle infinito.** Una tarea normalmente es un `for(;;)` o `while(1)`. Si la función llega al final y regresa, el comportamiento es indefinido (en muchos puertos el sistema se cuelga).
- **Terminar = borrarse.** Si una tarea ya no se necesita, llama a `vTaskDelete( NULL )`. `NULL` significa "esta misma tarea".
- **Variables locales por instancia.** Puedes crear varias tareas con la misma función; cada una tiene su propia pila, así que sus variables locales son independientes.
- **Variables `static` compartidas.** Una variable `static` dentro de la función es **una sola** para todas las instancias. Hay que protegerla si varias tareas la modifican.
- **Ceder el procesador.** Una tarea que nunca se bloquea (sin `vTaskDelay`, colas, semáforos) acapara el CPU e impide que corran las tareas de menor prioridad.

## 3. Estados de una tarea: Running y Not Running

En un microcontrolador de un solo núcleo (como el ATmega328), **solo una tarea puede estar en Running a la vez**. Todas las demás están en Not Running.

- **Running (en ejecución):** el procesador está ejecutando el código de esa tarea en este instante.
- **Not Running (no en ejecución):** la tarea existe, pero está "dormida". Su contexto (registros, contador de programa, pila) quedó guardado.

Cuando el scheduler saca a una tarea de Running, guarda su contexto (*switched out*). Cuando la vuelve a poner en Running, restaura el contexto (*switched in*) y la tarea **continúa exactamente en la instrucción donde se quedó**, como si nada hubiera pasado.

### Los sub-estados de Not Running

El estado Not Running se divide en tres sub-estados:

| Estado | Qué significa | Cómo entra | Cómo sale |
| --- | --- | --- | --- |
| **Ready (lista)** | Puede ejecutarse, pero hay otra tarea de igual o mayor prioridad en Running. | Al crearse, o al terminar su bloqueo. | El scheduler la elige: pasa a Running. |
| **Blocked (bloqueada)** | Espera un evento: un tiempo (`vTaskDelay`) o un recurso (cola, semáforo, notificación). No consume CPU. | Llama a una función bloqueante. | Ocurre el evento o vence el *timeout*: pasa a Ready. |
| **Suspended (suspendida)** | Fuera del scheduler hasta que alguien la reactive. No tiene timeout. | `vTaskSuspend()` | `vTaskResume()`: pasa a Ready. |

![Diagrama de estados de una tarea en FreeRTOS](diagrama_estados.png)

Running es el único estado que ejecuta código; Ready, Blocked y Suspended forman el estado Not Running. `vTaskSuspend()` también puede aplicarse a una tarea que está en Ready o Blocked.

### Regla del scheduler

FreeRTOS usa por defecto planificación **preemptiva con prioridades fijas**: siempre está en Running la tarea **Ready de mayor prioridad**. Si dos tareas Ready tienen la misma prioridad, se turnan en cada *tick* (time slicing).

La transición más importante para el alumno: una tarea solo pasa de Running a Ready o Blocked; **nunca va directo de Blocked a Running**, siempre pasa antes por Ready.

## 4. xTaskCreate(): crear una tarea

`xTaskCreate()` reserva memoria para la tarea (su TCB y su pila), la registra en el scheduler y la deja en estado **Ready**.

```c
BaseType_t xTaskCreate( TaskFunction_t      pvTaskCode,
                        const char * const  pcName,
                        uint16_t            usStackDepth,
                        void               *pvParameters,
                        UBaseType_t         uxPriority,
                        TaskHandle_t       *pxCreatedTask );
```

### Parámetros

| Parámetro | Tipo | Qué es | Ejemplo |
| --- | --- | --- | --- |
| `pvTaskCode` | `TaskFunction_t` | Puntero a la función de la tarea (solo su nombre, sin paréntesis). | `vTaskLed` |
| `pcName` | `const char *` | Nombre descriptivo. Solo sirve para depurar; el kernel no lo usa. Su largo máximo lo fija `configMAX_TASK_NAME_LEN`. | `"LED"` |
| `usStackDepth` | `uint16_t` | Tamaño de la pila en **palabras** (words), no en bytes. | `128` |
| `pvParameters` | `void *` | Valor que recibirá la tarea en su parámetro `pvParameters`. `NULL` si no pasas nada. | `(void *) &config` |
| `uxPriority` | `UBaseType_t` | Prioridad: de `0` (la más baja, la de la tarea Idle) a `configMAX_PRIORITIES - 1`. | `2` |
| `pxCreatedTask` | `TaskHandle_t *` | Salida opcional: aquí FreeRTOS escribe el *handle* de la tarea, para luego suspenderla, borrarla o cambiar su prioridad. `NULL` si no lo necesitas. | `&xHandleLed` |

### El tamaño de la pila

La pila real en bytes depende del ancho de palabra del procesador:

**bytes de pila = usStackDepth × sizeof(StackType_t)**

En un Cortex-M (32 bits) `StackType_t` ocupa 4 bytes, así que `128` palabras son 512 bytes. En el ATmega328 (8 bits) ocupa 1 byte, así que `128` son 128 bytes. Recuerda que el UNO solo tiene 2 KB de RAM: cada tarea cuenta. `configMINIMAL_STACK_SIZE` en `FreeRTOSConfig.h` es un buen punto de partida.

### Valor de retorno

- `pdPASS`: la tarea se creó correctamente.
- `errCOULD_NOT_ALLOCATE_REQUIRED_MEMORY` (equivale a `pdFAIL`): no hubo memoria en el *heap* de FreeRTOS para la pila y el TCB.

Siempre conviene revisarlo:

```c
if( xTaskCreate( vTaskLed, "LED", 128, NULL, 1, NULL ) != pdPASS )
{
    /* Error: falta heap. Reduce pilas o aumenta configTOTAL_HEAP_SIZE */
}
```

### Arrancar el scheduler

Crear tareas no las ejecuta. Las tareas empiezan a correr cuando arranca el scheduler con `vTaskStartScheduler()`, que normalmente nunca regresa. En **Arduino_FreeRTOS** el scheduler arranca solo al terminar `setup()`, así que no necesitas llamarlo.

## 5. Ejemplos con Arduino_FreeRTOS (ATmega328)

Todos los ejemplos usan la librería **FreeRTOS by Richard Barry** (Arduino_FreeRTOS), instalable desde el Library Manager del IDE de Arduino.

### Ejemplo 1: dos tareas independientes

Dos LEDs parpadean a ritmos distintos sin interferirse. Cada tarea se bloquea con `vTaskDelay()`, lo que deja el CPU libre para la otra.

```c
#include <Arduino_FreeRTOS.h>

void vTaskLed13( void *pvParameters );
void vTaskSerial( void *pvParameters );

void setup()
{
    Serial.begin( 9600 );

    xTaskCreate( vTaskLed13,  "LED13",  128, NULL, 1, NULL );
    xTaskCreate( vTaskSerial, "Serial", 128, NULL, 1, NULL );
    /* El scheduler arranca automáticamente al salir de setup() */
}

void loop() { /* vacío: aquí corre la tarea Idle */ }

void vTaskLed13( void *pvParameters )
{
    pinMode( 13, OUTPUT );
    for( ;; )
    {
        digitalWrite( 13, !digitalRead( 13 ) );
        vTaskDelay( 500 / portTICK_PERIOD_MS );
    }
}

void vTaskSerial( void *pvParameters )
{
    unsigned long n = 0;
    for( ;; )
    {
        Serial.println( n++ );
        vTaskDelay( 1000 / portTICK_PERIOD_MS );
    }
}
```

### Ejemplo 2: una función, dos tareas (uso de pvParameters)

La misma función crea dos tareas distintas. Cada una recibe por `pvParameters` su propio pin y periodo.

```c
#include <Arduino_FreeRTOS.h>

typedef struct
{
    uint8_t  pin;
    uint16_t periodo_ms;
} LedConfig_t;

/* static/global: deben seguir existiendo mientras corran las tareas */
static LedConfig_t ledRojo  = { 12, 250 };
static LedConfig_t ledVerde = { 11, 700 };

void vTaskBlink( void *pvParameters )
{
    LedConfig_t *cfg = ( LedConfig_t * ) pvParameters;   /* cast al tipo real */
    pinMode( cfg->pin, OUTPUT );

    for( ;; )
    {
        digitalWrite( cfg->pin, !digitalRead( cfg->pin ) );
        vTaskDelay( cfg->periodo_ms / portTICK_PERIOD_MS );
    }
}

void setup()
{
    xTaskCreate( vTaskBlink, "Rojo",  128, ( void * ) &ledRojo,  1, NULL );
    xTaskCreate( vTaskBlink, "Verde", 128, ( void * ) &ledVerde, 1, NULL );
}

void loop() {}
```

Punto clave: el dato apuntado por `pvParameters` debe **seguir vivo** mientras la tarea lo use. Por eso `ledRojo` y `ledVerde` son `static`; una variable local de `setup()` desaparecería al salir de la función.

### Ejemplo 3: prioridades y handle

Una tarea de prioridad 2 y otra de prioridad 1. Se guarda el handle de la tarea de baja prioridad para suspenderla y reanudarla.

```c
#include <Arduino_FreeRTOS.h>

TaskHandle_t xHandleBaja = NULL;

void vTaskAlta( void *pvParameters )
{
    for( ;; )
    {
        Serial.println( "ALTA: suspendo a BAJA" );
        vTaskSuspend( xHandleBaja );
        vTaskDelay( 2000 / portTICK_PERIOD_MS );

        Serial.println( "ALTA: reanudo a BAJA" );
        vTaskResume( xHandleBaja );
        vTaskDelay( 2000 / portTICK_PERIOD_MS );
    }
}

void vTaskBaja( void *pvParameters )
{
    for( ;; )
    {
        Serial.println( "  baja trabajando" );
        vTaskDelay( 300 / portTICK_PERIOD_MS );
    }
}

void setup()
{
    Serial.begin( 9600 );
    xTaskCreate( vTaskAlta, "Alta", 128, NULL, 2, NULL );
    xTaskCreate( vTaskBaja, "Baja", 128, NULL, 1, &xHandleBaja );
}

void loop() {}
```

Qué observar en el monitor serie: durante 2 s la tarea Baja no imprime nada (está **Suspended**); los otros 2 s imprime cada 300 ms. Mientras las dos están en `vTaskDelay()` ambas están **Blocked**, y corre la tarea Idle.

**Experimento sugerido:** quita el `vTaskDelay()` de `vTaskAlta`. Como es la tarea de mayor prioridad y nunca se bloquea, la tarea Baja (y la Idle) ya no vuelven a ejecutarse: es el fenómeno de **inanición** (*starvation*).

## 6. Errores comunes, glosario y ejercicios

### Errores comunes

| Síntoma | Causa probable | Solución |
| --- | --- | --- |
| El programa se reinicia o se cuelga al crear tareas | Pila demasiado pequeña (*stack overflow*) o falta de heap. | Aumenta `usStackDepth`; revisa el retorno de `xTaskCreate()`; activa `configCHECK_FOR_STACK_OVERFLOW`. |
| Solo corre una tarea | La tarea de mayor prioridad nunca se bloquea. | Agrega `vTaskDelay()` o espera en una cola/semáforo. |
| La tarea lee basura en `pvParameters` | Se pasó la dirección de una variable local que ya no existe. | Usa variables `static`, globales o memoria dinámica. |
| Comportamiento errático al final de la tarea | La función de la tarea hizo `return`. | Bucle infinito, o `vTaskDelete( NULL )` antes de salir. |
| `xTaskCreate()` devuelve error | No cabe en `configTOTAL_HEAP_SIZE`. | Menos tareas, pilas más chicas o más heap. |
| `delay()` de Arduino bloquea todo | `delay()` es una espera activa que no cede el CPU. | Dentro de tareas usa siempre `vTaskDelay()`. |

### Glosario

| Término | Definición |
| --- | --- |
| Tarea (task) | Función de C con bucle infinito que el kernel ejecuta con su propia pila y prioridad. |
| Scheduler | Parte del kernel que decide qué tarea Ready pasa a Running. |
| TCB | *Task Control Block*: estructura donde el kernel guarda el estado, prioridad y puntero de pila de cada tarea. |
| Contexto | Registros del CPU, contador de programa y puntero de pila de una tarea. |
| Cambio de contexto | Guardar el contexto de la tarea saliente y restaurar el de la entrante. |
| Tick | Interrupción periódica que usa el kernel para medir tiempo y repartir el CPU. |
| Handle | Identificador (`TaskHandle_t`) para referirse a una tarea desde otras funciones. |
| Tarea Idle | Tarea de prioridad 0 que el kernel crea automáticamente; corre cuando nadie más está Ready. |
| Preempción | El scheduler quita el CPU a una tarea en cuanto otra de mayor prioridad está Ready. |

### Ejercicios para los alumnos

- [ ] Escribe una función de tarea que imprima su nombre, recibido por `pvParameters` como `char *`. Crea tres instancias con nombres distintos.
- [ ] Modifica el Ejemplo 1 para que ambas tareas usen `delay()` en vez de `vTaskDelay()`. Explica qué cambia y por qué.
- [ ] Crea dos tareas con prioridades 1 y 2, ambas sin `vTaskDelay()`. Predice cuál corre y compruébalo.
- [ ] Usa `uxTaskGetStackHighWaterMark( NULL )` dentro de una tarea para medir cuánta pila le sobra. Ajusta `usStackDepth` al mínimo seguro.
- [ ] Dibuja el diagrama de estados (Running, Ready, Blocked, Suspended) y anota qué función de la API provoca cada transición.
- [ ] Crea una tarea que haga 5 parpadeos y luego se borre con `vTaskDelete( NULL )`.
