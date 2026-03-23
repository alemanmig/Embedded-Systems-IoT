###
### ¿Cuando trabajar con multiprocesamiento o multi hilo?
#
## ¿Tenemos un equipo con varios procesaodres?


# Al utilizar multihilos estamos compartiendo un mismo espaso de memoria
# Se ejecutan al mismo tiempo las tareas pero en tiempos distinto

# El el multiprocesamiento si se pueden ejecutar las tareas de manera simultanea
# Cada proceso es procesado en un nucleo del procesador

# Para trabajar con multiprocesamiento en Puython usaremos 
# import multiprocessing

import multiprocessing
import time

# Paso 1

def algo():
    print("Inicial proceso")
    time.sleep(5)
    print("Finbaliza proceso")

# necesitamos utilizar un bloque que nos permita condicionar la seccion del codigo
# que se encargará de crear los procesos

proceso = multiprocessing.Process(target=algo)
proceso.start()
print("Finalizar proceso padre")

# This probably means that you are not using fork to start your
#       child processes and you have forgotten to use the proper idiom
#       in the main module:
#
#            if __name__ == '__main__':    <-------- Necesitaremos esto
#                freeze_support()

# Paso 2
# Comentar lineas 29, 30 y 31 y descomentar 43 a 46 

#if __name__ == '__main__':         # Como solo tenemos un proceso lo podemos correr desde aqui
#    proceso = multiprocessing.Process(target=algo)
#    proceso.start()
#    print("Finalizar proceso padre")

# Ceeamos un proceso usando multiprocessing
