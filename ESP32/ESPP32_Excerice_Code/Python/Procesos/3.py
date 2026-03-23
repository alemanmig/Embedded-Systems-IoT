# Procesos demonio
# Procesos que detendran suejecución, una vez que el proceso padre 
# temine su ejecución

import multiprocessing
import time

def conteo(cantidad):
    for i in range(cantidad):
        time.sleep(0.5)
        print(i)

if __name__ == "__main__":
    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad":20}, daemon=False)
    proceso.start()
    print("Finaliza proceso padre")

#if __name__ == "__main__":
#    proceso = multiprocessing.Process(target=conteo, kwargs={"cantidad":20}, daemon=True)
#    proceso.start()
#    time.sleep(5)
#    print("Finaliza proceso padre")

