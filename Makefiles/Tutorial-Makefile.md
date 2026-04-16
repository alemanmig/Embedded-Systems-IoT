# Tutorial de Makefile

## Que es un Makefile

Un `Makefile` es un archivo de automatizacion usado por la herramienta `make`. Sirve para definir tareas, dependencias y comandos que deben ejecutarse para construir, probar, limpiar o desplegar un proyecto.

En lugar de escribir manualmente muchos comandos en la terminal, puedes dejar todo descrito en un solo archivo. Luego ejecutas:

```bash
make
```

o una tarea especifica:

```bash
make clean
make run
make plot
```

## Para que sirve

Con un `Makefile` puedes automatizar procesos como:

- Compilar programas en C o C++.
- Ejecutar pruebas.
- Limpiar archivos temporales.
- Generar reportes o graficas.
- Ejecutar scripts.
- Copiar archivos a otra carpeta.
- Programar un microcontrolador o una FPGA.
- Encadenar un flujo completo de compilacion, simulacion y ejecucion.

## Estructura basica

La forma general de una regla en un `Makefile` es:

```make
objetivo: dependencias
	comando
```

Ejemplo:

```make
programa: main.o
	g++ main.o -o programa
```

Aqui:

- `programa` es el objetivo.
- `main.o` es la dependencia.
- `g++ main.o -o programa` es el comando que se ejecuta.

Importante:

- El comando debe comenzar con una tabulacion real, no con espacios.
- Si una dependencia cambia, `make` vuelve a construir solo lo necesario.

## Componentes principales de un Makefile

### 1. Variables

Las variables ayudan a evitar repetir texto y facilitan cambios futuros.

```make
CXX = g++
CXXFLAGS = -std=c++23 -O3
APP = julia
SRCS = main.cpp
OBJS = $(SRCS:.cpp=.o)
```

En este ejemplo:

- `CXX` guarda el compilador.
- `CXXFLAGS` guarda las banderas de compilacion.
- `APP` es el nombre del ejecutable.
- `SRCS` contiene los archivos fuente.
- `OBJS` convierte automaticamente `main.cpp` en `main.o`.

### 2. Objetivos

Un objetivo representa un archivo a generar o una tarea a ejecutar.

```make
all: run plot open
```

Cuando ejecutas `make` sin argumentos, normalmente se ejecuta el primer objetivo del archivo. En este caso, seria `all`.

### 3. Dependencias

Las dependencias indican que un objetivo necesita otros archivos o tareas antes de ejecutarse.

```make
run: $(APP)
	./$(APP)
```

Aqui `run` depende de `$(APP)`. Si el ejecutable no existe o esta desactualizado, primero se recompila.

### 4. Reglas de patron

Sirven para definir reglas genericas.

```make
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@
```

Esto significa:

- cualquier archivo `.o` se puede construir a partir de su correspondiente `.cpp`.

Variables automaticas usadas aqui:

- `$<` = primera dependencia.
- `$@` = nombre del objetivo.

### 5. Objetivos `.PHONY`

Se usan para tareas que no representan archivos reales.

```make
.PHONY: clean run
```

Esto evita conflictos si existe un archivo con el mismo nombre que el objetivo.

### 6. Comandos

Son las instrucciones que `make` ejecuta en la terminal.

```make
clean:
	rm *.o $(APP) *.txt *.png
```

## Analisis del Makefile de este proyecto

El archivo [Makefile](C:/Users/alema/Documents/alemanmig/Embedded-Systems-IoT/Makefiles/julia/Makefile) contiene este flujo:

1. Compila `main.cpp` a `main.o`.
2. Enlaza `main.o` para crear el ejecutable `julia`.
3. Ejecuta el programa para generar `julia_set.txt`.
4. Usa `gnuplot` para crear `julia_set.png`.
5. Abre la imagen generada.

Ese flujo muestra bien una idea central de `make`: automatizar una secuencia completa a partir de dependencias.

## Ejemplo explicado paso a paso

### Variables del proyecto

```make
CXX = g++
CXXFLAGS = -std=c++23 -O3
GP = julia_set.gp
TXT = $(GP:.gp=.txt)
PNG = $(GP:.gp=.png)
SRCS = main.cpp
OBJS = $(SRCS:.cpp=.o)
APP = julia
```

Estas lineas definen nombres reutilizables. Si cambias el compilador o agregas archivos fuente, el mantenimiento es mas facil.

### Objetivo principal

```make
all: run plot open
```

Este objetivo dice: para completar `all`, primero deben ejecutarse `run`, `plot` y `open`.

### Compilacion de objetos

```make
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@
```

Si existe `main.cpp`, esta regla permite generar `main.o`.

### Enlace

```make
$(APP): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(APP)
```

Si existe `main.o`, esta regla genera el ejecutable final.

### Ejecucion

```make
run: $(APP)
	./$(APP)
```

Primero se asegura de que el ejecutable exista. Luego lo corre.

### Generacion de grafica

```make
plot: $(TXT)
	gnuplot $(GP)
```

Esto sirve para convertir los datos producidos por el programa en una imagen.

### Limpieza

```make
clean:
	rm *.o $(APP) *.txt *.png
```

Este objetivo elimina archivos generados para dejar el directorio limpio.

## Que se puede automatizar con un Makefile

Un `Makefile` no se limita a compilar. Tambien puede automatizar procesos completos de ingenieria.

### Ejemplos comunes

- Compilar firmware.
- Convertir archivos fuente en binarios `.elf`, `.hex` o `.bin`.
- Correr pruebas unitarias.
- Ejecutar simulaciones.
- Generar documentacion.
- Programar una tarjeta de desarrollo.
- Abrir un monitor serial.
- Empaquetar resultados.

## Como automatizar un proceso de programacion

Si trabajas en sistemas embebidos o IoT, un flujo tipico puede ser:

1. Compilar el codigo.
2. Generar el archivo binario.
3. Cargarlo al microcontrolador.
4. Abrir una terminal serial para ver la salida.

### Ejemplo de Makefile para automatizar firmware

```make
CC = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
CFLAGS = -mcpu=cortex-m4 -mthumb -O2
TARGET = app
SRCS = main.c gpio.c uart.c
OBJS = $(SRCS:.c=.o)

.PHONY: all flash monitor clean

all: $(TARGET).bin

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET).elf: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

flash: $(TARGET).bin
	st-flash write $(TARGET).bin 0x8000000

monitor:
	pio device monitor -b 115200

clean:
	rm -f *.o *.elf *.bin
```

### Que hace este ejemplo

- `make` compila todo y genera `app.bin`.
- `make flash` programa el microcontrolador.
- `make monitor` abre el monitor serial.
- `make clean` borra archivos generados.

Esto reduce errores humanos y hace repetible el proceso.

## Buenas practicas

- Usa variables para compiladores, banderas y nombres de archivos.
- Declara objetivos `.PHONY` para tareas como `clean`, `run` o `flash`.
- Divide el flujo en objetivos pequenos y claros.
- Evita repetir comandos.
- Usa dependencias reales para que `make` reconstruya solo lo necesario.
- Agrega un objetivo `help` si el proyecto tiene muchas tareas.

## Ejemplo de objetivo help

```make
.PHONY: help

help:
	@echo "Objetivos disponibles:"
	@echo "  make        -> compilar el proyecto"
	@echo "  make run    -> ejecutar el programa"
	@echo "  make clean  -> borrar archivos generados"
```

## Limitaciones y detalles importantes

- `make` funciona especialmente bien en proyectos con archivos y dependencias claras.
- En Windows, algunos comandos como `rm` o `xdg-open` pueden no existir. En ese caso debes cambiarlos por equivalentes como `del` o `start`, o usar entornos como MSYS2, Git Bash o WSL.
- Los comandos de cada regla se ejecutan en una shell.
- La tabulacion al inicio del comando es obligatoria en un `Makefile` tradicional.

## Version mejorada del Makefile de este proyecto

El `Makefile` actual funciona, pero se puede hacer mas portable y claro. Por ejemplo:

```make
CXX = g++
CXXFLAGS = -std=c++23 -O3
APP = julia
SRCS = main.cpp
OBJS = $(SRCS:.cpp=.o)
GP = julia_set.gp
TXT = julia_set.txt
PNG = julia_set.png

.PHONY: all run plot clean vars

all: run plot

vars:
	@echo "SRCS = $(SRCS)"
	@echo "OBJS = $(OBJS)"
	@echo "APP  = $(APP)"

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

$(APP): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@

$(TXT): $(APP)
	./$(APP)

plot: $(TXT) $(GP)
	gnuplot $(GP)

run: $(APP)
	./$(APP)

clean:
	rm -f *.o $(APP) $(TXT) $(PNG)
```

Mejoras en esta version:

- `plot` depende tambien del archivo `.gp`.
- `$(TXT)` se genera explicitamente a partir de `$(APP)`.
- `clean` usa `rm -f`.
- `all` evita abrir automaticamente una ventana externa.

## Resumen

Un `Makefile` permite describir tareas en forma declarativa:

- que quieres construir,
- de que depende,
- y que comando debe ejecutarse.

La mayor ventaja es que convierte procesos manuales en flujos repetibles y rapidos.

En tu proyecto, el `Makefile` ya automatiza:

- compilacion,
- ejecucion,
- generacion de datos,
- graficacion.

Ese mismo enfoque se puede extender a procesos de programacion de sistemas embebidos, pruebas y despliegue.

## Ejercicio recomendado

Como practica, puedes intentar agregar a tu `Makefile`:

1. Un objetivo `help`.
2. Un objetivo `rebuild` que haga `clean` y luego `all`.
3. Un objetivo `flash` simulado que imprima el comando que usarias para programar una tarjeta.

Ejemplo:

```make
.PHONY: rebuild flash

rebuild: clean all

flash:
	@echo "Aqui iria el comando para programar el dispositivo"
```

## Cierre

Si quieres, en el siguiente paso puedo hacer una segunda version de este tutorial:

- mas corta, para exponer en clase,
- mas formal, para entregar como reporte,
- o mas practica, basada por completo en tu carpeta `julia`.
