### Pre-requisitos:

Tener instalado Docker en el equipo donde se ejecutará el software.

&#x09;- Si aún no lo tienes instalado, descárgalo e instálalo desde el sitio oficial: https://www.docker.com/



#### ***1- Creación del archivo Dockerfile***

Nota: Estos pasos deben realizarse desde la ruta donde está ubicada la aplicación de Docker.<br /><br />a. Abrir PowerShell en el equipo.<br />	Acceder a la ruta donde está ubicada la aplicación que deseas ejecutar dentro del contenedor Docker.<br />	Puedes usar el comando cd para moverte entre carpetas.<br />	cd C:\\ruta\\de\\tu\\aplicacion<br /><br />b. Crear un archivo llamado Dockerfile (sin extensión).<br />	Comando creacion: New-Item -Name Dockerfile -ItemType File.<br />	Aperturar archivo: notepad Dockerfile, se abrirá el Notepad.<br /><br />c. Agregar el siguiente contenido al archivo:<br />	# 1. Imagen base estable<br />	FROM ubuntu:22.04<br /><br />	# 2. Configuración de entorno no interactivo<br />	ENV DEBIAN\_FRONTEND=noninteractive<br /><br />	# 3. Dependencias gráficas y de compilación<br />	RUN apt-get update \&\& apt-get install -y \\<br />   	build-essential \\<br />    	g++ \\<br />    	gnuplot \\<br />    	xdg-utils \\<br />    	libx11-dev \\<br />    	\&\& rm -rf /var/lib/apt/lists/\*<br /><br />	# 4. Directorio de trabajo genérico<br />	WORKDIR /usr/src/app<br /><br />	# 5. Copiamos el contenido del proyecto<br />	COPY . .<br /><br />	# 6. Variable para el comando por defecto (Ej: 'all', 'run', etc.)<br />	ARG MAKE\_TARGET=all<br />	ENV TARGET=$MAKE\_TARGET<br /><br />	# 7. Variable de entorno para X11<br />	ENV XDG\_RUNTIME\_DIR=/tmp<br /><br />	# 8. Ejecutamos el Makefile con el target deseado<br />	CMD make ${TARGET}







#### ***2. Construcción de la imagen Docker***

a. Verifica que te encuentres ubicado en la carpeta donde se encuentra tu archivo Dockerfile<br />	ej. cd "......\\Docker\\Docker\\Docker Desktop.exe"<br />	\* Puedes usar PowerShell para moverte con el comando cd hacia el directorio correcto.<br /><br />	Nota: No debes moverte a la carpeta donde está instalado Docker Desktop.<br /><br />	-- Información adicional: ---------------------<br />	Docker Desktop debe estar corriendo y/o activo.<br />	Esto significa que la API de Docker debe estar funcionando.<br />	Si no está activo, aparecerán errores como:<br />		“Cannot connect to the Docker daemon” o "ERROR: failed to the Docker API... "<br /><br />b. Ejecuta el siguiente comando: ---<br />docker build -t ambiente\_c\_mas\_mas .<br />------------------------------------<br />	-- Información adicional: ----------------------------------------------------------------------------------------<br />	Explicación del comando: docker build -t ambiente\_c\_mas\_mas .<br />	docker build → indica a Docker que construya una nueva imagen.<br /><br />	-t ambiente\_c\_mas\_mas → asigna un nombre (tag) a la imagen, en este caso ambiente\_c\_mas\_mas.<br /><br />	. → el punto significa que se usará el Dockerfile que está en el directorio actual.<br /><br />	Este proceso descargará la imagen base de Ubuntu 22.04, instalará las dependencias y configurará el entorno según lo 	definido en tu Dockerfile.<br />	Al finalizar, tendrás lista la imagen que servirá como contenedor de trabajo.<br /><br />	\* Posible WARNING durante la construcción de la imagen<br />	Durante el proceso de construcción de la imagen Docker, puede aparecer el siguiente mensaje:<br /> 	1. WARNING (NO PASA nada puede continuar)<br />	1 warning found (use docker --debug to expand):<br />	- JSONArgsRecommended: JSON arguments recommended for CMD to prevent unintended behavior related to OS signals (line 	30)}<br /><br />		-- ¿Qué significa este WARNING?<br />		Es únicamente una recomendación de Docker.<br /><br />		Sugiere usar el formato JSON en la instrucción CMD del Dockerfile.<br /><br />		No afecta la creación de la imagen ni la ejecución del contenedor.<br /><br />		Puedes continuar sin problema.<br /><br />		Motivo del WARNING<br />		El Dockerfile utiliza la instrucción: CMD make ${TARGET}<br />		Docker recomienda el formato JSON, por ejemplo: CMD \["make", "${TARGET}"]<br />		Sin embargo, no es obligatorio realizar este cambio.<br />		El contenedor funcionará correctamente con la instrucción actual.<br />	------------------------------------------------------------------------------------------------------------<br />



#### ***3. Creación del Proyecto***

<br />Las instrucciones descritas a continuación aplican para cada proyecto en C o C++ que vayamos a crear. Para comenzar a trabajar dentro del contenedor Docker, es necesario contar con una carpeta que contenga tu proyecto o los archivos fuente que deseas compilar o ejecutar.<br /><br /><br />a. Creación de la carpeta del proyecto<br />	Puedes crear esta carpeta en cualquier ruta de tu equipo.<br />	No es necesario que esté ubicada donde se encuentra el API de Docker ni donde está instalado Docker Desktop.<br /><br />	Lo importante es que luego puedas acceder a esta carpeta desde PowerShell para construir la imagen y ejecutar el contenedor.<br />	<br />	<br />	Crear la carpeta por línea de comando (PowerShell)<br />	Abrir PowerShell.<br />	Ejecutar el siguiente comando para crear la carpeta del proyecto: EJ. mkdir ProyectoJulia<br />	Acceder a la carpeta recién creada: ej. cd ProyectoJulia<br /><br />***Estructura del Proyecto<br />***Dentro de la carpeta del proyecto (EJ. ProyectoJulia) crearemos la siguiente estructura:<br />1. Carpeta ***src*** (Obligatoria)<br />	En esta carpeta debe ir todo el código fuente del proyecto, incluyendo:<br />	Archivos .cpp<br />	Archivos .c<br />	Archivos .h<br />	Cualquier otro archivo relacionado con la lógica del programa<br />	Esta carpeta es indispensable porque el Makefile tomará los archivos desde aquí para compilar.<br /><br />2. Archivo ***Makefile*** (Obligatorio) <br />	\**\*\* Este archivo se creará más adelante siguiendo las instrucciones indicadas en el manual. **→ dirígete a la instrucción 2.A<br />***	Este archivo define:<br />	Las reglas de compilación<br />	Las reglas de limpieza (por ejemplo, eliminar archivos .o)<br />	Opcionalmente, reglas de ejecución del proyecto<br />	<br />	El Makefile es fundamental para que Docker pueda ejecutar: make all<br />	o cualquier otro target que definas.<br /><br />3. Carpeta **scripts** (Opcional)<br />	Esta carpeta se utiliza para colocar programas auxiliares relacionados con el proyecto, como:<br />	Scripts de pruebas<br />	Scripts de automatización<br />	Archivos de graficación<br />	Herramientas adicionales<br />	Para el caso de estudio ej. ProyectoJulia, dentro de esta carpeta colocaremos:<br />	julia\_set.gp → Script de gnuplot que permite graficar la salida generada por el código en C++.<br />



#### ***2.A Crear un archivo llamado Makefile (sin extensión).***

Comando creacion: New-Item -Name Makefile -ItemType File<br />Aperturar archivo: notepad Makefile, se abrirá el Notepad.<br /><br />Agregar el siguiente contenido al archivo:<br />#==============================================================================<br />#CONFIGURACIÓN DE RUTAS<br />#==============================================================================<br />CXX      := g++<br />#Este es nuestro compilador seleccionado g++, puede ser cualquier otro como clang++<br />CXXFLAGS := -std=c++23 -O3 -Wall <br />#Aqui colocamos banderas utiles para el compilador<br /><br />#A partir de esta linea definimos la estructura de nuestro directorio de trabajo:<br /><br /># Directorios de Código y Herramientas<br />SRC\_DIR     := src<br />SCRIPT\_DIR  := scripts<br />#Creacion automatica (no existen hasta compilar y ejecutar)<br />OBJ\_DIR     := obj<br />BIN\_DIR     := bin<br />OUT\_DIR     := output<br /><br /># Archivos de Compilación<br />#Ejecutable<br />APP         := $(BIN\_DIR)/julia<br />SOURCES     := $(wildcard $(SRC\_DIR)/\*.cpp)<br />OBJECTS     := $(SOURCES:$(SRC\_DIR)/%.cpp=$(OBJ\_DIR)/%.o)<br /><br /># Archivos de Proceso (Rutas relativas para Gnuplot)<br />GP\_SCRIPT   := $(SCRIPT\_DIR)/julia\_set.gp<br />DATA\_FILE   := $(OUT\_DIR)/julia\_set.txt<br />IMAGE\_FILE  := $(OUT\_DIR)/julia\_set.png<br /><br />#==============================================================================<br />#REGLAS DE EJECUCIÓN<br />#==============================================================================<br />#Esta es la ejecucion por default de make, es decir si solo escribimos make esto es lo que ejecutaremos por default.<br />all: prepare $(APP) run plot show\_info<br /><br />#Esta linea es auxiliar y permite a make no confundir reglas con archivos o directorios<br />.PHONY: all prepare run plot clean show\_info<br /><br />#A parti de este punto definimos las acciones a realizar por make, y que "encadenandolas" nos permite compilar, limpiar, o probar nuestro proyecto <br /><br /># Crea la estructura de carpetas si no existe<br />prepare:<br />	@mkdir -p $(OBJ\_DIR) $(BIN\_DIR) $(OUT\_DIR) $(SCRIPT\_DIR)<br /><br /># Compilación de objetos<br />$(OBJ\_DIR)/%.o: $(SRC\_DIR)/%.cpp<br />	@echo "  \[CC]  $< -> $@"<br />	@$(CXX) $(CXXFLAGS) -c $< -o $@<br /><br /># Enlazado del binario<br />$(APP): $(OBJECTS)<br />	@echo "  \[LD]  Creando binario: $@"<br />	@$(CXX) $(CXXFLAGS) $(OBJECTS) -o $@<br /><br /># Ejecución del parograma C++<br />run: $(APP)<br />	@echo "  \[RUN] Generando datos en $(DATA\_FILE)..."<br />	@./$(APP)<br /><br /># Ejecución de Gnuplot (le pasamos el script desde su carpeta)<br />plot: $(DATA\_FILE)<br />	@echo "  \[GP]  Procesando script: $(GP\_SCRIPT)..."<br />	@gnuplot $(GP\_SCRIPT)<br /><br />show\_info:<br />	@echo "-------------------------------------------------------"<br />	@echo "✅ Proceso Finalizado."<br />	@echo "📂 Binario: $(APP)"<br />	@echo "🖼️  Imagen:  $(IMAGE\_FILE)"<br />	@echo "-------------------------------------------------------"<br /><br />clean:<br />	@echo "  \[CLEAN] Borrando carpetas generadas..."<br />	@rm -rf $(OBJ\_DIR) $(BIN\_DIR) $(OUT\_DIR)<br />


#### **4. Ejecución del contenedor Docker**

Una vez creada la imagen en el paso anterior, ahora pondremos a trabajar nuestro “laboratorio de compilación” de C++ dentro de Docker.<br /><br />Para ello, ejecutamos el siguiente comando desde PowerShell, ubicados en la carpeta del proyecto:<br />docker run -ti --rm -v "${PWD}:/usr/src/app" ambiente\_c\_mas\_mas<br /><br />	-- Información adicional: -- Explicación detallada del comando -----------------------------------------<br />	-ti<br />	Activa el modo interactivo.<br />	Permite ver en tiempo real:<br />	Mensajes del Makefile<br />	Errores de compilación<br />	Progreso de gnuplot<br />	Cualquier salida del programa<br />	Es decir, te “mete” dentro del contenedor como si fuera una consola normal.<br /><br />	--rm<br />	Significa “limpieza automática”.<br />	Cuando el proceso termina, el contenedor se destruye.<br />	Esto evita que se acumulen contenedores viejos en tu disco.<br />	La imagen permanece, solo se elimina el contenedor temporal.<br /><br />	-v "${PWD}:/usr/src/app"<br />	Este parámetro define un volumen (storage compartido).<br />	${PWD} → carpeta actual en Windows<br />	/usr/src/app → carpeta de trabajo dentro del contenedor<br /><br />	Resultado:<br />	Todo lo que el programa genere dentro de Docker aparece automáticamente en tu carpeta de Windows.<br /><br />	Ejemplo:<br />	Si tu código C++ genera salida.png dentro del contenedor, ese archivo aparecerá en tu carpeta local.<br /><br />	ambiente\_c\_mas\_mas<br />	Es el nombre de la imagen creada en el paso anterior.<br />	Puedes cambiarlo si usaste otro nombre.<br />	--------------------------------------------------------------------------------------------------------<br /><br /><br />NOTA IMPORTANTE<br />A veces puede parecer que los archivos no se actualizan dentro del volumen compartido.<br />En esos casos, un comando útil es:<br />docker run --rm -v "${PWD}:/usr/src/app" ambiente\_c\_mas\_mas make clean<br /><br />Este comando funciona como un reset del volumen, eliminando archivos temporales y permitiendo que el proyecto se sincronice correctamente.





## Flujo de Trabajo Final

El flujo de trabajo típico para desarrollar y probar proyectos en C/C++ dentro del contenedor Docker es el siguiente:



* Modificar el código en la carpeta src

&#x09;Aquí puedes cambiar colores en gnuplot, fórmulas matemáticas, mensajes de salida, etc.



* Ejecutar el contenedor con el comando de Docker

&#x09;powershell

&#x09;docker run -ti --rm -v "${PWD}:/usr/src/app" ambiente\_c\_mas\_mas

* Ver el resultado

&#x09;Los archivos generados aparecerán en la carpeta output/ (si tu Makefile los define allí).

&#x09;También puedes ver resultados directamente por la salida estándar en la consola.



Importante

No es necesario hacer docker build cada vez.  

El volumen (-v) se encarga de que Docker siempre use la versión más reciente de tus archivos locales.



Cualquier proyecto en cualquier ubicación puede ser ejecutado en el contenedor.

El único requisito es que el Makefile tenga definida correctamente la regla por defecto (all).

Ejemplo: proyecto squareDigits.





Entrar al contenedor manualmente

Si deseas entrar directamente al contenedor para ejecutar comandos de forma interactiva, utiliza:

docker run -ti --rm -v "${PWD}:/usr/src/app" ambiente\_c\_mas\_mas /bin/bash



Esto abrirá una consola bash dentro del contenedor, permitiéndote:

Navegar por los archivos del proyecto.

Ejecutar manualmente make, gnuplot u otros comandos.

Probar configuraciones sin necesidad de salir y volver a correr el contenedor.

