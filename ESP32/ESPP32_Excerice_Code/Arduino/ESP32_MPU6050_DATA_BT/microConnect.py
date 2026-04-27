from threading import Thread
import serial
import time
import sys

class SerialData:
    def __init__(self, port, baud=9600):
        self.port = port
        self.baud = baud

        self.isRun = True
        self.thread = None
        
        print('Trying to connect to: ' + str(self.port))
        try:
            self.serialConnection = serial.Serial(self.port, self.baud)
            print('Connected to ' + str(self.port))
        except Exception as e:
            sys.exit("Failed to connect with " + str(self.port) + ": " + str(e))
    
    def startRead(self, sizeData=1):
        """
        Inicia la lectura de datos en un hilo separado.
        
        :param sizeData: Número de datos a leer al recibir 'E'.
        """
        if self.thread is None:
            self.sizeData = sizeData
            self.rawData = [None] * self.sizeData
            self.thread = Thread(target=self.backgroundRead)
            self.thread.start()

    def backgroundRead(self):
        """Lee datos del puerto serie en un hilo separado."""
        while self.isRun:
             if self.serialConnection.in_waiting > 0:
                  line = self.serialConnection.readline().strip().decode("utf-8")
                  if line == "E":  # Iniciar lectura al recibir 'E'
                       for k in range(self.sizeData):
                            try:
                                 self.rawData[k] = float(self.serialConnection.readline().strip())
                            except ValueError:
                                 print(f"Error: Data received is not a valid float at index {k}.")
                                 self.rawData[k] = None

    def sendData(self, dataToSend, separator=','):
        """Envía datos al puerto serie, separados por el carácter especificado."""
        stringData = separator.join(map(str, dataToSend))
        self.serialConnection.write((stringData + '\n').encode())

    def close(self):
        """Cierra la conexión serie y espera a que el hilo de lectura termine."""
        self.isRun = False
        if self.thread is not None:
            self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')

if __name__ == "__main__":
    main()

