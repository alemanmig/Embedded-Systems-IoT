# Reutilización de procesos
# Este ejemplo muestra cómo reutilizar procesos para ejecutar varias tareas sin tener que crear un nuevo proceso para cada tarea. Esto es útil para mejorar el rendimiento y reducir el tiempo de ejecución, especialmente cuando las tareas son cortas y se pueden ejecutar en paralelo.
# En este ejemplo, se crean tres funciones de suma que simulan tareas que tardan un tiempo en completarse. Luego, se utiliza ProcessPoolExecutor para ejecutar estas funciones en paralelo y obtener los resultados cuando estén disponibles. El bloque with se encarga de gestionar el ciclo de vida de los procesos, asegurando que se cierren correctamente después de su uso. 
# Al final, se imprime "Fin" para indicar que el programa ha terminado, pero los resultados de las sumas se imprimirán a medida que cada proceso termine su tarea.

from concurrent.futures import ProcessPoolExecutor
import time

def suma1(a, b):
    time.sleep(5)
    return a + b   

def suma2(a, b):
    time.sleep(1)
    return a + b

def suma3(a, b):
    time.sleep(1)
    return a + b    

def resultado(futuro):
    print("El resultado de la suma es: ", futuro.result())


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=3) as executor:
        futuro1 = executor.submit(suma1, 5, 10)
        futuro1.add_done_callback(resultado)

        futuro2 = executor.submit(suma2, 50, 1)
        futuro2.add_done_callback(resultado)

        futuro3 = executor.submit(suma3, 38, 15)
        futuro3.add_done_callback(resultado)

    # Esperamos a que los procesos terminen
    # El bloque with se encarga de esperar a que todos los procesos terminen antes de continuar
    # No es necesario llamar a executor.shutdown() explícitamente, ya que el bloque with lo hace automáticamente
    # Si queremos esperar a que un proceso específico termine, podemos usar futuro.result() o futuro.done()
    # futuro1.result()  # Espera a que el proceso de suma1 termine

    # Para evitar el uso del bloque with, podríamos hacer lo siguiente:
    # comentar el bloque with y crear el executor sin él (linea 23 - 31)
    
    # decomentar de la linea 43 a la 48 y comentar el bloque with (linea 23 - 31)
    # executor = ProcessPoolExecutor(max_workers=3)
    # futuro1 = executor.submit(suma1, 5, 10)
    # futuro1.add_done_callback(resultado)

    # futuro2 = executor.submit(suma2, 50, 1)
    # futuro2.add_done_callback(resultado)

    # futuro3 = executor.submit(suma3, 38, 15)
    # futuro3.add_done_callback(resultado)

    # Esperamos a que los procesos terminen
    # executor.shutdown()
    # Como no usamos el bloque with, debemos llamar a executor.shutdown() para esperar a que todos los procesos terminen antes de continuar
    # Si queremos esperar a que un proceso específico termine, podemos usar futuro.result() o
    #  futuro.done()
    # si no finalizamos el proceso con shutdown(), el programa puede terminar antes de que los procesos terminen, lo que puede causar errores o resultados inesperados


    print("Fin")