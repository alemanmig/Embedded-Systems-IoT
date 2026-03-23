
import multiprocessing
import time

def evaluacion(lista, queue):
    res=[]
    for i in lista:
        time.sleep(1)
        if i == "Azul":
            res.append(1)
        else:
            res.append(0)
    queue.put(res)

if __name__ == "__main__":
    queue1 = multiprocessing.Queue()
    queue2 = multiprocessing.Queue()
    lista1 = ["Azul", "Rojo", "Azul", "Azul"] # simula la lectura de los sensores
    lista2 = ["Azul", "Azul", "Azul", "Azul"] 
    proceso1 = multiprocessing.Process(target=evaluacion, kwargs={"lista":lista1, "queue:":queue1,}, daemon=True)
    proceso2 = multiprocessing.Process(target=evaluacion, kwargs={"lista":lista1, "queue:":queue1,}, daemon=True)
    proceso1.start()
    proceso2.start()

    time.sleep(2)
    res1 = queue1.get_nowait()
    res2 = queue2.get_nowait()

    print(res1)

    if all(res1) and all(res2):
        print("Resultado OK")
    else:
        print("Resultado NO OK")
