# Docker y Contenedores

Docker es una plataforma que permite empaquetar aplicaciones con sus dependencias, librerías, configuraciones y entorno de ejecución dentro de unidades portables llamadas contenedores. Esto facilita que una aplicación funcione de forma consistente en diferentes equipos, sistemas operativos y etapas del ciclo de desarrollo.

## ¿Qué es Docker?

Docker utiliza virtualización ligera basada en contenedores. A diferencia de una máquina virtual tradicional, un contenedor no necesita incluir un sistema operativo completo; comparte el kernel del sistema anfitrión y aísla procesos, red, almacenamiento y configuración.

Esto hace que los contenedores sean:

- Más rápidos de crear e iniciar.
- Más ligeros en consumo de recursos.
- Más fáciles de mover entre entornos.
- Más consistentes entre desarrollo, pruebas y producción.

## Capacidades principales de Docker

Docker ofrece varias capacidades importantes para el desarrollo y despliegue de software:

- Empaquetado reproducible de aplicaciones.
- Aislamiento de procesos y dependencias.
- Portabilidad entre equipos y servidores.
- Automatización de builds mediante `Dockerfile`.
- Versionado de imágenes por capas.
- Ejecución de servicios en segundo plano o interactivos.
- Exposición y mapeo de puertos.
- Persistencia de datos mediante volúmenes.
- Comunicación entre contenedores por redes internas.
- Escalabilidad y orquestación en entornos más grandes.

## Conceptos clave

### Imagen

Una imagen es una plantilla inmutable que contiene todo lo necesario para ejecutar una aplicación: sistema base, paquetes, archivos y configuración.

### Contenedor

Un contenedor es una instancia en ejecución de una imagen. Puede iniciarse, detenerse, eliminarse y recrearse tantas veces como sea necesario.

### Dockerfile

Es un archivo de texto con instrucciones para construir una imagen. Permite automatizar el proceso de instalación, copiado de archivos, configuración de variables y definición del comando de arranque.

### Volúmenes

Los volúmenes permiten persistir datos fuera del ciclo de vida del contenedor. Son útiles para bases de datos, archivos generados, logs o carpetas de trabajo compartidas.

### Redes

Docker permite conectar contenedores entre sí sin exponer necesariamente todos los servicios al exterior. Esto facilita arquitecturas con frontend, backend, base de datos, caché y otros componentes distribuidos.

## Posibilidades para crear contenedores

Docker no se limita a un solo caso de uso. Se puede utilizar para construir contenedores con distintos objetivos:

- Aplicaciones web con servidores como Nginx, Node.js, Python, Java o PHP.
- APIs y microservicios desacoplados.
- Entornos de compilación para C, C++, Rust, Go o Java.
- Laboratorios de pruebas y validación de software.
- Herramientas de automatización y CI/CD.
- Bases de datos y servicios auxiliares.
- Aplicaciones de análisis de datos o procesamiento batch.
- Entornos docentes o de laboratorio reproducibles.
- Aplicaciones con dependencias complejas difíciles de instalar localmente.

## Ventajas de trabajar con contenedores

- Reducen el clásico problema de "en mi máquina sí funciona".
- Facilitan la colaboración entre equipos.
- Simplifican la distribución del entorno completo.
- Permiten destruir y recrear entornos sin afectar el sistema base.
- Mejoran la consistencia entre desarrollo, testing y producción.
- Hacen más sencillo escalar servicios o dividir responsabilidades.

## Limitaciones y consideraciones

Aunque Docker es muy útil, conviene tener en cuenta algunos puntos:

- Los contenedores no sustituyen por completo a las máquinas virtuales.
- El manejo de datos persistentes requiere planificación.
- Algunas aplicaciones gráficas o con acceso especial a hardware necesitan configuración adicional.
- La seguridad depende también de cómo se construyen y ejecutan las imágenes.
- En Windows y macOS, Docker corre sobre una capa adicional de virtualización.

## Flujo básico de trabajo

1. Escribir un `Dockerfile`.
2. Construir una imagen con `docker build`.
3. Crear y ejecutar un contenedor con `docker run`.
4. Ver logs, acceder al contenedor o detenerlo según sea necesario.
5. Repetir el proceso al cambiar el código o la configuración.

## Ejemplo aplicado a este proyecto

Este repositorio incluye un `Dockerfile` orientado a compilar y ejecutar un proyecto sobre `Ubuntu 22.04`. La imagen instala herramientas como:

- `build-essential`
- `g++`
- `gnuplot`
- `xdg-utils`
- `libx11-dev`

Después copia el contenido del proyecto al contenedor, define el directorio de trabajo en `/usr/src/app` y utiliza una variable `TARGET` para decidir qué objetivo de `make` ejecutar.

El comando final es:

```dockerfile
CMD make ${TARGET}
```

Eso significa que el contenedor está preparado para actuar como entorno de compilación y ejecución automatizado.

## Ejemplo de uso con este Dockerfile

Construir la imagen:

```bash
docker build -t docker-workspace .
```

Construir la imagen indicando un target específico:

```bash
docker build --build-arg MAKE_TARGET=all -t docker-workspace .
```

Ejecutar el contenedor:

```bash
docker run --rm docker-workspace
```

Si deseas montar el proyecto local dentro del contenedor para trabajar con archivos persistentes:

```bash
docker run --rm -v ${PWD}:/usr/src/app docker-workspace
```

## Caso práctico en este repositorio

En la carpeta `ejemplo` hay un flujo basado en `Makefile` que:

- Compila un programa en C++.
- Genera datos.
- Ejecuta `gnuplot`.
- Produce una imagen final.

Este es un buen ejemplo de cómo Docker puede encapsular un entorno técnico con compilador, utilidades y dependencias gráficas sin exigir instalación manual en la máquina anfitriona.

## Conclusión

Docker permite construir entornos repetibles, portables y aislados para casi cualquier tipo de aplicación. Su mayor valor está en convertir configuraciones complejas en procesos declarativos, reproducibles y fáciles de compartir. En proyectos como este, también sirve para estandarizar herramientas de compilación y ejecución, reduciendo fricción entre equipos y máquinas distintas.
