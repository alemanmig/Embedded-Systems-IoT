# Ejercicio de programación con hilos en Pytho

import time
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import current_thread

def imprimirValor():
    time.sleep(0.3)
    print("Hola Mundo")

#ejecucion secuencial
# for i in range(15):
#     imprimirValor()

#ejecucucion concurrente
# for i in range(15):
#     hilo = threading.Thread(target=imprimirValor)
#     hilo.start()

#def imprimir1():
#    time.sleep(0.3)
#    print("Ejecutnado hilo 1")
#
#def imprimir2():
#    time.sleep(0.3)
#    print("Ejecutnado hilo 2")
#
#def imprimir3():
#    time.sleep(0.3)
#    print("Ejecutnado hilo 3")
#
#hilo1 = threading.Thread(target=imprimir1)
#hilo2 = threading.Thread(target=imprimir2)
#hilo3 = threading.Thread(target=imprimir3)
#hilo1.start()
#hilo2.start()
#hilo3.start()

def sumar(a,b):
    print(a+b)

#hilo = threading.Thread(target=sumar, args=[5,9])
#hilo.start()

#hilo = threading.Thread(target=sumar, args=(5,9))
#hilo.start()

#hilo = threading.Thread(target=sumar, args=(5,))
#hilo.start()

#hilo = threading.Thread(target=sumar, kwargs={"a":5,"b":9})
#hilo.start()

#def dormir():
#    time.sleep(5)
#    print("desperte")

#hilo = threading.Thread(target=dormir)
#hilo.start()

#for i in range(500):
#    time.sleep(0.1)
#    print(i)

#def prueba1():
#    time.sleep(3)
#    return 5

#def prueba2():
#    time.sleep(2.5)
#    return 3
#
#def prueba3():
#    time.sleep(1)
#    return 8
#
#x = prueba1()
#y = prueba2()
#z = prueba3()

#if x == 5 and y == 3 and z == 8:
#    print("Rsultado OK")
#
#else: 
#    print("Resultado NO OK")

#def prueba1():
#    global x
#    time.sleep(3)
#    x = 5
#    print("Terminada 1")

#def prueba2():
#    global y
#    time.sleep(2.5)
#    y = 3
#    print("Terminada 2")

#def prueba3():
#    global z
#    time.sleep(1)
#    print("Terminada 3")
#    z = 8

#x = 0
#y = 0
#z = 0

#hilo1 = threading.Thread(target=prueba1)
#hilo2 = threading.Thread(target=prueba2)
#hilo3 = threading.Thread(target=prueba3)
#hilo1.start()
#hilo2.start()
#hilo3.start()

#if x == 5 and y == 3 and z == 8:
#    print("Rsultado OK")

#else: 
#    print("Resultado NO OK")

#def prueba1():
#    global x
#    time.sleep(3)
#    x = 5
#    print("Terminada 1")

#def prueba2():
#    global y
#    time.sleep(2.5)
#    y = 3
#    print("Terminada 2")

#def prueba3():
#    global z
#    time.sleep(1)
#    print("Terminada 3")
#    z = 8

#x = 0
#y = 0
#z = 0

#hilo1 = threading.Thread(target=prueba1)
#hilo2 = threading.Thread(target=prueba2)
#hilo3 = threading.Thread(target=prueba3)
#hilo1.start()
#hilo2.start()
#hilo3.start()
#hilo1.join()
#hilo2.join()
#hilo3.join()

#if x == 5 and y == 3 and z == 8:
#    print("Rsultado OK")

#else: 
#    print("Resultado NO OK")

#def prueba1():
#    while True:
#        print("Estoy ejecutandome")
#        time.sleep(0.01)

#hilo = threading.Thread(target=prueba1)
#hilo.start()
#print("hola")

#def prueba1():
#    while True:
#        print("Estoy ejecutandome")
#        time.sleep(0.01)

#hilo = threading.Thread(target=prueba1, daemon=True)
#hilo.start()
#print("hola")

#lock = threading.Lock()
#a = 0
#
#def sumar():
#    global a
#    for i in range(0, 10000000):
#        with lock:
#            a += 1
#
#def restar():
#    global a
#    for i in range(0, 10000000):
#        with lock:
#            a -= 1
#
#hilo1 = threading.Thread(target=sumar)
#hilo2 = threading.Thread(target=restar)
#hilo1.start()
#hilo2.start()
#hilo1.join()
#hilo2.join()
#
#print(a)
#

#def ciclar(evento1, evento2):
#    while not evento2.is_set():
#        print("ciclo while")
#        evento1.wait()
#
#evento1 = threading.Event()
#evento2 = threading.Event()
#hilo = threading.Thread(target=ciclar, args=(evento1, evento2))
#hilo.start()
#
#for i in range(5):
#    time.sleep(5)
#    print("Realizando el ciclo for")

#evento1.set()
#time.sleep(1)
#evento2.set()

# Ejemplo con 2 ciclos While
# Sincronizar Eventos

#def ciclar1 (evento1, evento3):
#    while not evento3.is_set():
#        evento1.wait()
#        print("Nuevo ciclo del while 1")
#        evento1.clear()
#        time.sleep(0.1)

#def ciclar2 (evento2, evento3):
#    while not evento3.is_set():
#        evento1.wait()
#        print("Nuevo ciclo del while 2")
#        evento2.clear()
#        time.sleep(0.1)

#evento1 = threading.Event()
#evento2 = threading.Event()
#evento3 = threading.Event()
#hilo1 = threading.Thread(target=ciclar1, args=(evento1, evento2))
#hilo2 = threading.Thread(target=ciclar2, args=(evento2, evento3))
#hilo1.start()
#hilo2.start()

#for i in range(5):
#    evento1.set()
#    time.sleep(0.1)
#    evento2.set()
#    time.sleep(0.1)

#evento3.set()

#def ciclar(evento1):
#    print("presione para liberar la señal\n")
#    resp = evento1.wait(timeout=10)
#    if resp == True:
#        print("sistema de enfriamiento disparado de forma manual\n")
#    else:
#        print("sistema de enfriamiento disparado de forma automática\n")

#evento1 = threading.Event()
#hilo = threading.Thread(target=ciclar, args=(evento1, ))
#hilo.start()

#print("Esperando para enviar la señal")
#time.sleep(3)
#evento1.set() #comentar esta linea
#time.sleep(1)

# Reutilización de hilos o threads
# from concurrent.futures import ThreadPoolExecutor
# from threading import current_thread

#def suma(a,b):
#    time.sleep(0.1)
#    thread = current_thread()
#    print(thread.name) 
#    print(a+b, "\n")

#executor = ThreadPoolExecutor(max_workers=2)
#executor.submit(suma, 15,37)
#executor.submit(suma, 34,2)
#executor.submit(suma, 5,3)
#executor.submit(suma, 55,34)
#executor.submit(suma, 55,32)

#Como liberar los hilos

#def suma(a,b):
#    time.sleep(0.1)
#    thread = current_thread()
#    print(thread.name) 
#    print(a+b, "\n")

#executor = ThreadPoolExecutor(max_workers=2)
#executor.submit(suma, 15,37)
#executor.submit(suma, 34,2)
#executor.submit(suma, 5,3)
#executor.submit(suma, 55,34)
#executor.submit(suma, 55,32)

#executor.shutdown()
#executor.submit(suma, 10,10)

#def suma(a,b):
#    time.sleep(5)
#    return a+b

#executor = ThreadPoolExecutor(max_workers=2)
#futuro = executor.submit(suma, 15,37)
#print(futuro.result())

#def suma(a,b):
#    time.sleep(5)
#    return a+b

#executor = ThreadPoolExecutor(max_workers=2)
#futuro = executor.submit(suma, 15,37)
#for i in range(15):
#    print(futuro.result())

def suma(a,b):
    time.sleep(1)
    return a+b

def fin(futuro):
    print("finalizo la ejecución")
    print(futuro.result())

executor = ThreadPoolExecutor(max_workers=2)
futuro = executor.submit(suma, 15,37)
futuro.add_done_callback(fin)

for i in range(15):
    time.sleep(0.2)
    print(i)