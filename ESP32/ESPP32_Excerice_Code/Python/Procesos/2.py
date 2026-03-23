
import multiprocessing
import time

def suma(a,b):
    print("El resultado es: ", a+b)

# Paso 1
# (Utilizando una tupla)

#if __name__ == "__main__":
#    proceso1 = multiprocessing.Process(target=suma, args=(10,25))
#    proceso2 = multiprocessing.Process(target=suma, args=(5,5))
#    proceso3 = multiprocessing.Process(target=suma, args=(2,3))
#    proceso1.start()
#    proceso2.start()
#    proceso3.start()

# Paso 2
# Utilizando un diccionario
# comentar de la fila 12 - 17

if __name__ == "__main__":
    proceso1 = multiprocessing.Process(target=suma, kwargs={"a":10,"b":25})
    proceso2 = multiprocessing.Process(target=suma, kwargs={"a":5,"b":5})
    proceso3 = multiprocessing.Process(target=suma, kwargs={"a":2,"b":3})
    proceso1.start()
    proceso2.start()
    proceso3.start()



