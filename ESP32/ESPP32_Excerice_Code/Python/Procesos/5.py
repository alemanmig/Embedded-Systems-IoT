
# Ejercicio de trabajo con join
# Nos funciona para hacer que el proceso padre se detenga a esperar
# a que el proceso hijo termine su ejecución

import multiprocessing
import time

def conteo(cantidad,queue):
    for i in range(cantidad):
        time.sleep(0.5)
        print(i)
        queue.put("hola"+str(i))

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad":20, "queue":queue}, daemon=True)
    proceso.start()
    time.sleep(5)
    print("Termina sleep")
    proceso.join()
    print("Finaliza proceso padre")
    while not queue.empty():
        print(queue.get())

# esto podría servirnos en la parte de programación concurrente
# si tenemo pruebas de 2 distintos sensores y necesitamos que teminen de hacer
# las mediciones y despues realice la evaluacoión

