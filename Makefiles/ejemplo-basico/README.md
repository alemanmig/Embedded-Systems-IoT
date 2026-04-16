# Ejemplo basico de Makefile

Este ejemplo muestra un flujo minimo para automatizar compilacion y ejecucion.

## Archivos

- `main.c`: programa de ejemplo.
- `Makefile`: reglas para compilar, ejecutar y limpiar.

## Comandos

```bash
make help
make
make run
make clean
make rebuild
```

## Que demuestra

- Uso de variables.
- Uso de dependencias.
- Regla patron `%.o: %.c`.
- Objetivos `.PHONY`.
- Automatizacion de un flujo basico de programacion.
