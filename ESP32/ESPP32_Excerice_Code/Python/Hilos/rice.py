
import time
import threading

a = 0

def sumar():
    global a
    for i in range(0,10000000):
        a +=1

def restar():
    global a
    for i in range(0,10000000):
        a -= 1

hilo1 = threading.Thread(target=sumar)
hilo2 = threading.Thread(target=restar)
hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print(a)
