#Sensor de Temperatura con ESP32

import dht   #biblioteca para usar los sensores DHT11/DHT22
from machine import Pin  #permite configurar pines GPIO del microcontrolador
import time  #se usa para esperar entre lecturas

sensor = dht.DHT22(Pin(15)) #Se crea un objeto sensor del tipo DHT22
                            #El sensor está conectado al pin GPIO 15

while True:                 #bucle infinito
    try:                    #Bloque try–except para manejar errores
        sensor.measure()    #ordena al DHT22 que haga una medición
        temp = sensor.temperature()   #devuelve la temperatura en °C
        humidity = sensor.humidity()  #devuelve la humedad en %
        print(f'Temperature: {temp} C degree Humidity: {humidity} %')
    except OSError as e:             #Si algo sale mal (sensor desconectado, cable suelto, ruido eléctrico)
        print('Failed to read Sensor') #MicroPython lanza un OSError, y se captura en el except para evitar que el programa se detenga.

    time.sleep(2)   #Se espera 2 segundos.
                    #El DHT22 NO se puede leer más rápido de 0.5 Hz (una lectura cada 2 segundos aprox.)
                    #de lo contrario fallaría.