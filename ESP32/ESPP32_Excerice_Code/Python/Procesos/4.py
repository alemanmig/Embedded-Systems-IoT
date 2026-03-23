
# Dentro del multiprocesamiento tambien podemos ocupar Queues 
# Nos sirve para tetornar elementos desde la función que se encuentra
# en el proceso que hemos creado.

import multiprocessing
import time

#def conteo(cantidad,queue):
#    for i in range(cantidad):
#        time.sleep(0.5)
#        print(i)
#        queue.put(i)

#if __name__ == "__main__":
#    queue = multiprocessing.Queue()
#    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad":20, "queue":queue}, daemon=True)
#    proceso.start()
#    time.sleep(5)
#    print("Finaliza proceso padre")
#    while not queue.empty():
#        print(queue.get())

# Paso 2
# comentar de la 9 a la 22

#def conteo(cantidad,queue):
#    for i in range(cantidad):
#        time.sleep(0.5)
#        print(i)
#        queue.put("hola"+str(i))

#if __name__ == "__main__":
#    queue = multiprocessing.Queue()
#    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad":20, "queue":queue}, daemon=True)
#    proceso.start()
#    time.sleep(5)
#    print("Finaliza proceso padre")
#    while not queue.empty():
#        print(queue.get())