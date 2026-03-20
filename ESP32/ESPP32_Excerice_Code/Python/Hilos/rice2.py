
import time
import threading

lock = threading.Lock()
a = 0

def sumar():
    global a
    for i in range(0,10000000):
        lock.acquire()
        a +=1
        lock.release()

def restar():
    global a
    for i in range(0,10000000):
        lock.acquire()
        a -= 1
        lock.release()

hilo1 = threading.Thread(target=sumar)
hilo2 = threading.Thread(target=restar)
hilo1.start()
hilo2.start()
hilo1.join()
hilo2.join()

print(a)