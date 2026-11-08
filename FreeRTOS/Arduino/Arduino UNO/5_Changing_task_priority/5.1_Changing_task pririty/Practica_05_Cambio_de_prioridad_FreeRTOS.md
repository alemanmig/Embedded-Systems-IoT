# Práctica 05: Cambio de prioridad de tareas en FreeRTOS

Nov 8, 2026 · @Miguel

## Objetivos

Al terminar esta práctica el alumno observará en tres LEDs cómo la prioridad de una tarea decide quién usa la CPU en FreeRTOS.

1. Crear tres tareas con `xTaskCreate()` y guardar sus *handles*.
2. Consultar la prioridad de una tarea con `uxTaskPriorityGet()`.
3. Cambiar la prioridad en tiempo de ejecución con `vTaskPrioritySet()`.
4. Distinguir entre una tarea que **bloquea** (cede la CPU) y una que hace **espera activa** (la retiene).
5. Explicar el *time slicing* entre tareas de igual prioridad y la inanición (*starvation*) de las tareas de menor prioridad.

## Material y conexiones

| Material | Cantidad | Nota |
| --- | --- | --- |
| Arduino UNO | 1 | Con cable USB |
| LED rojo | 1 | Pin digital 6 |
| LED amarillo | 1 | Pin digital 7 |
| LED azul | 1 | Pin digital 8 |
| Resistencia 220 Ω a 330 Ω | 3 | Una en serie con cada LED |
| Protoboard y cables | 1 juego | — |

Software: Arduino IDE 2.3.x y la librería **FreeRTOS** de Richard Barry / Phillip Stevens (feilipu), versión 11.1.0-3, instalada desde el Gestor de Librerías.

Conexión de cada LED: pin digital → resistencia → ánodo (pata larga) → cátodo (pata corta) → GND.

## Marco teórico

En FreeRTOS el planificador (*scheduler*) siempre ejecuta la tarea **lista** de **mayor prioridad**; la prioridad solo importa cuando dos o más tareas compiten por la CPU al mismo tiempo.

### Estados de una tarea

| Estado | Significado | Ejemplo |
| --- | --- | --- |
| Running | Está usando la CPU ahora mismo | Solo una tarea a la vez en el UNO |
| Ready | Puede ejecutarse, espera su turno | Una tarea en espera activa que perdió su turno |
| Blocked | Espera un evento o un tiempo; no consume CPU | Una tarea dentro de `vTaskDelay()` |
| Suspended | Detenida explícitamente con `vTaskSuspend()` | No se usa en esta práctica |

### Prioridades

- Cada tarea tiene un número de prioridad: 0 es la más baja (la usa la tarea **Idle**).
- En esta librería `configMAX_PRIORITIES` vale 4, así que las prioridades válidas son 0, 1, 2 y 3.
- Si una tarea de prioridad 2 está lista, ninguna de prioridad 1 se ejecuta. A esto se le llama **inanición** (*starvation*).

### Time slicing

Cuando varias tareas listas tienen la **misma** prioridad, el planificador las alterna en cada *tick* del sistema. En la librería de feilipu el tick lo genera el **Watchdog Timer** y dura unos **15 ms**. Por eso tres tareas de prioridad 1 parecen ejecutarse “al mismo tiempo”.

### Bloqueo contra espera activa

- **Bloqueo** (`vTaskDelay()`): la tarea pasa a *Blocked* y libera la CPU. Es la forma correcta en un sistema real, pero oculta el efecto de la prioridad porque casi nunca hay competencia.
- **Espera activa** (*busy-wait*): la tarea gira en un ciclo vacío consultando `millis()`. Sigue en *Ready/Running* y compite por la CPU todo el tiempo. Es lo que usamos aquí para **hacer visible** la prioridad.
- Importante: en esta librería la función `delay()` de Arduino está redefinida para llamar a `vTaskDelay()`, así que **también bloquea**. No sirve para generar competencia.

### La tarea Idle y loop()

Al terminar `setup()` la librería arranca el planificador automáticamente. La función `loop()` se ejecuta dentro de la tarea **Idle**, de prioridad 0. Si ninguna otra tarea se bloquea nunca, `loop()` prácticamente no se ejecuta.

## Código del sketch

Crea un sketch nuevo llamado `Changing_task_priority`, copia el código completo y guárdalo antes de compilar.

```cpp
#include <Arduino_FreeRTOS.h>

#define RED    6
#define YELLOW 7
#define BLUE   8

#define STACK_SIZE     128   // En el port AVR la pila se mide en BYTES
#define BLINK_MS       200   // Medio periodo de parpadeo
#define TOGGLES_CAMBIO 20    // 20 x 200 ms = 4 s entre cambios de prioridad

TaskHandle_t red_Handle    = NULL;
TaskHandle_t blue_Handle   = NULL;
TaskHandle_t yellow_Handle = NULL;

// Espera activa: ocupa la CPU SIN ceder el control al planificador.
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

      vTaskPrioritySet(NULL, nueva);
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
  // El planificador arranca solo al terminar setup().
}

void loop()
{
  // Se ejecuta dentro de la tarea Idle (prioridad 0).
}
```

## Explicación del código

El programa crea tres tareas iguales en prioridad 1; cada 4 s la tarea amarilla alterna su propia prioridad entre 1 y 2, y eso congela o libera a las otras dos.

### 1. Inclusión de la librería y definiciones

- `#include <Arduino_FreeRTOS.h>` incorpora el núcleo de FreeRTOS. Basta con incluirla: la librería arranca el planificador sola después de `setup()`.
- `RED`, `YELLOW` y `BLUE` dan nombre a los pines 6, 7 y 8.
- `STACK_SIZE` es el tamaño de pila de cada tarea. En el port para AVR se mide en **bytes**. El UNO solo tiene 2 KB de RAM, así que cada byte cuenta.
- `BLINK_MS` fija cuánto dura cada estado del LED (encendido o apagado).
- `TOGGLES_CAMBIO` indica cada cuántos cambios del LED amarillo se modifica la prioridad: 20 × 200 ms = 4 s.

### 2. Handles de tarea

Un `TaskHandle_t` es una referencia a una tarea ya creada. `xTaskCreate()` lo llena en su último parámetro. Con él, cualquier parte del programa puede consultar, cambiar, suspender o borrar esa tarea.

### 3. La función busyWait()

Guarda el valor de `millis()` y gira en un `while` vacío hasta que pasen `ms` milisegundos. Durante ese tiempo la tarea **no se bloquea**: sigue lista y compitiendo por la CPU.

`millis()` sigue funcionando con FreeRTOS porque el tick del sistema usa el Watchdog Timer y deja libre el Timer0, que es el que alimenta a `millis()`. La resta `millis() - t0` también funciona correctamente cuando el contador se desborda.

### 4. Tareas roja y azul

- Su firma `void tarea(void *pvParameters)` es la que exige FreeRTOS para toda tarea.
- `(void) pvParameters;` evita el aviso de “parámetro no usado”.
- `for (;;)` es un ciclo infinito: **una tarea nunca debe terminar con `return`**.
- `digitalWrite(PIN, !digitalRead(PIN))` invierte el estado del LED. En el AVR, leer un pin configurado como salida devuelve el último valor escrito.

### 5. Tarea amarilla: el cambio de prioridad

- Hace lo mismo que las otras, pero cuenta sus cambios en `toggles`.
- Al llegar a 20 consulta su prioridad con `uxTaskPriorityGet(NULL)`. El `NULL` significa “la tarea que está llamando”.
- Calcula la nueva prioridad con el operador ternario: si es 1 pasa a 2, si es 2 vuelve a 1.
- Imprime el cambio por el puerto serie. `Serial.flush()` espera a que salga todo el texto antes de continuar.
- `vTaskPrioritySet(NULL, nueva)` aplica el cambio de inmediato. Si la tarea **baja** su prioridad, FreeRTOS revisa en ese momento si hay otra tarea lista con igual o mayor prioridad y le cede la CPU.

### 6. setup()

- Inicializa el puerto serie y los tres pines como salida, **antes** de que existan las tareas.
- Crea las tres tareas con `xTaskCreate()`. Sus parámetros, en orden, son:

| Parámetro | Valor en el sketch | Para qué sirve |
| --- | --- | --- |
| Función de la tarea | `redLedControllerTask` | Código que ejecuta la tarea |
| Nombre | `"RED"` | Solo para depuración |
| Tamaño de pila | `STACK_SIZE` (128 bytes) | Memoria para variables locales y llamadas |
| Parámetro | `NULL` | Dato que recibe en `pvParameters` |
| Prioridad | `1` | Prioridad inicial |
| Handle | `&red_Handle` | Dónde se guarda la referencia a la tarea |

- Cada llamada se compara con `pdPASS`. Si falla, casi siempre es por falta de memoria (heap) y el monitor serie lo indica.

### 7. loop()

Queda vacía. Corre dentro de la tarea Idle (prioridad 0), que en este programa casi nunca recibe CPU porque las tres tareas de prioridad 1 o 2 nunca se bloquean.

## Procedimiento y resultados esperados

El programa repite un ciclo de 8 s: 4 s con los tres LEDs activos y 4 s con solo el amarillo.

1. Arma el circuito de la sección Material y conexiones. Revisa la polaridad de cada LED.
2. Abre Arduino IDE, selecciona **Herramientas → Placa → Arduino Uno** y el puerto correcto.
3. Copia el sketch, compílalo y anota el uso de memoria RAM que reporta el IDE.
4. Súbelo a la placa.
5. Abre el Monitor Serie a **9600 baudios**.
6. Observa los LEDs durante al menos dos ciclos completos (unos 16 s) y compáralos con la tabla.

| Tiempo | Prioridad del amarillo | LED rojo | LED azul | LED amarillo | Monitor serie |
| --- | --- | --- | --- | --- | --- |
| 0 – 4 s | 1 | Parpadea | Parpadea | Parpadea | `Tareas creadas. Todas con prioridad 1.` |
| 4 – 8 s | 2 | Congelado | Congelado | Parpadea | `Amarillo: prioridad 1 -> 2` |
| 8 – 12 s | 1 | Parpadea | Parpadea | Parpadea | `Amarillo: prioridad 2 -> 1` |
| 12 – 16 s | 2 | Congelado | Congelado | Parpadea | `Amarillo: prioridad 1 -> 2` |

“Congelado” significa que el LED se queda fijo, encendido o apagado, en el estado en que lo dejó su tarea al perder la CPU. No se apaga: simplemente nadie lo vuelve a cambiar.

Si algún LED nunca enciende, revisa primero la polaridad y la resistencia. Si el monitor muestra un mensaje de error de creación de tarea, falta memoria.

## Preguntas de análisis

Responde cada pregunta con base en lo que observaste, no solo en la teoría.

1. ¿Por qué los LEDs rojo y azul dejan de parpadear cuando el amarillo tiene prioridad 2, si sus tareas no se han borrado ni suspendido?
2. ¿En qué estado (Running, Ready o Blocked) se encuentran las tareas roja y azul durante los 4 s en que están congeladas?
3. ¿Cómo logran parpadear los tres LEDs “a la vez” si el UNO tiene un solo núcleo? Relaciona tu respuesta con el tick de 15 ms.
4. ¿Por qué la tarea amarilla puede regresar a prioridad 1 aunque las otras dos no se estén ejecutando?
5. ¿Qué ventaja tiene usar `NULL` en `uxTaskPriorityGet()` y `vTaskPrioritySet()` en lugar de `yellow_Handle`?
6. ¿Por qué se usa `busyWait()` y no `delay()` para el parpadeo? ¿Qué cambiaría en un sistema real?
7. ¿Qué pasa con `loop()` y la tarea Idle mientras se ejecuta este programa?

## Ejercicios de modificación

Cada ejercicio cambia una o dos líneas del sketch original; antes de subirlo, **escribe tu predicción**, luego compárala con lo que observas y explica la diferencia. Regresa al código original antes de pasar al siguiente ejercicio.

### Ejercicio 1. Ritmo y periodo de cambio

Cambia `BLINK_MS` a `500` y `TOGGLES_CAMBIO` a `10`.

- Calcula cada cuántos segundos debería cambiar la prioridad.
- Mide el tiempo con un cronómetro y compáralo con tu cálculo.

### Ejercicio 2. Prioridad 3 en lugar de 2

En la tarea amarilla cambia la línea del ternario por:

```cpp
UBaseType_t nueva = (actual == 1) ? 3 : 1;
```

- ¿Cambia algo en los LEDs? ¿Qué te dice esto sobre si la prioridad es un valor absoluto o relativo?
- ¿Qué pasaría si escribieras `5`? Consulta `configMAX_PRIORITIES`.

### Ejercicio 3. Una tarea que nace con mayor prioridad

Regresa al código original y en `setup()` crea la tarea **roja** con prioridad `2`:

```cpp
xTaskCreate(redLedControllerTask, "RED", STACK_SIZE, NULL, 2, &red_Handle);
```

- ¿Qué LEDs parpadean? ¿Llega a aparecer algún mensaje de cambio de prioridad en el monitor serie? ¿Por qué?

### Ejercicio 4. Bloquear en lugar de esperar activamente

En la tarea **amarilla** reemplaza `busyWait(BLINK_MS);` por:

```cpp
vTaskDelay(pdMS_TO_TICKS(BLINK_MS));
```

- Cuando el amarillo tiene prioridad 2, ¿se congelan el rojo y el azul? Explica por qué el resultado cambia, usando los estados de tarea.
- Esta es la forma correcta de escribir tareas en un sistema real. ¿Por qué?

### Ejercicio 5. Cambiar la prioridad de otra tarea

En la tarea amarilla cambia la llamada por:

```cpp
vTaskPrioritySet(red_Handle, nueva);
```

- Ahora el amarillo intenta cambiar la prioridad de la tarea **roja**. ¿Qué observas después de los primeros 4 s? ¿Se recupera el sistema? Justifica.
- ¿Para qué sirve guardar los handles en `setup()`?

### Ejercicio 6. ¿Cuándo corre loop()?

Agrega `pinMode(LED_BUILTIN, OUTPUT);` en `setup()` y escribe dentro de `loop()`:

```cpp
digitalWrite(LED_BUILTIN, HIGH);
```

- ¿Se enciende el LED integrado (pin 13)?
- Repite el ejercicio 4 aplicándolo a las **tres** tareas. ¿Qué cambia con el LED 13 y por qué?

### Reto opcional. Ajustar la pila

Al final del ciclo de la tarea amarilla imprime cuánta pila le queda sin usar:

```cpp
Serial.println(uxTaskGetStackHighWaterMark(NULL));
```

- Con ese dato, ¿podrías reducir `STACK_SIZE`? ¿Cuánto margen dejarías y por qué? Prueba un valor y verifica que el programa siga funcionando.

## Entregables y evaluación

Entrega un reporte breve con evidencia de cada parte; el peso de cada criterio aparece en la tabla.

| Entregable | Evidencia | Peso |
| --- | --- | --- |
| Circuito y programa base funcionando | Video de 15 s o más que muestre un ciclo completo de los LEDs | 20 % |
| Captura del Monitor Serie | Al menos dos cambios de prioridad visibles | 10 % |
| Preguntas de análisis | Respuestas a las 7 preguntas, con tus propias palabras | 30 % |
| Ejercicios de modificación | Por cada ejercicio: línea modificada, predicción, resultado observado y explicación | 35 % |
| Reto opcional | Valor del *high water mark* y tamaño de pila elegido | +5 % extra |
| Conclusión | Un párrafo: cuándo conviene bloquear y cuándo importa la prioridad | 5 % |
