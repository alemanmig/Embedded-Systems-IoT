from microConnect import *
import collections
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkinter import *
import copy
import serial.tools.list_ports  # Importar para listar puertos

# Variables Globales
isCollect = False
collectData = []
labelData = []
samples = 100
sampleTime = 100
data = []
sizeData = 3  # Cambia esto según sea necesario

# Inicialización de datos
for i in range(sizeData):
    data.append(collections.deque([0] * samples, maxlen=samples))

xmin = 0
xmax = samples
ymin = -15
ymax = 15

lines = []
lineValueText = []

# Crear gráfica
fig = plt.figure()
ax = plt.axes(xlim=(xmin, xmax), ylim=(ymin, ymax))
plt.title('Monitoreo en tiempo real')
plt.grid()
ax.set_xlabel('Muestras')
ax.set_ylabel('Medida')

for i in range(sizeData):
    lines.append(ax.plot([], [], label='signal' + str(i))[0])
    lineValueText.append(ax.text(0.65, 0.90 - i * 0.05, '', transform=ax.transAxes))

plt.legend(loc="upper left")

# Función para listar puertos disponibles
def list_ports():
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

# Abrir puerto serial
serialComm = None

def open_serial_comm():
    global serialComm
    selected_port = port_var.get()
    baudRate = int(baud_var.get())
    serialComm = SerialData(selected_port, baudRate)
    serialComm.startRead(sizeData)
    print_to_text(f"Puerto {selected_port} abierto con {baudRate} baudios.")

def start():
    global isCollect
    isCollect = True
    print_to_text("Recolectando Clase " + entry.get() + " con etiqueta " + entryLabel.get())

def pause():
    global isCollect
    isCollect = False
    print_to_text("Pausado")

def delete():
    global isCollect, collectData, labelData
    isCollect = False
    collectData.clear()
    labelData.clear()
    print_to_text("Clase "+entry.get()+" borrada")

def save():
    global isCollect
    isCollect = False
    
    file_name = 'P'+ entry.get() + '.npy'
    try:
        with open(file_name, 'wb') as f:
            np.save(f, collectData)
        print_to_text(f"{file_name} guardado")
    except Exception as e:
        print_to_text(f"Error al guardar el archivo: {e}")
        
    file_name = 'T'+ entry.get() + '.npy'
    try:
        with open(file_name, 'wb') as f:
            labelData_n = np.array(labelData)
            np.save(f, labelData_n.reshape(-1, 1))
        print_to_text(f"Etiqueta " + entryLabel.get() + " guardada")
    except Exception as e:
        print_to_text(f"Error al guardar el archivo: {e}")

    delete()

def onClosing():
    root.quit()  # Luego cerrar la interfaz
    if serialComm:
        serialComm.close()  # Cerrar la comunicación serial primero
    root.destroy()
    

def print_to_text(message):
    """Muestra un mensaje en el widget de texto."""
    text_widget.insert(END, message + '\n')
    text_widget.see(END)  # Desplazarse hacia abajo

def plotData(frame, lines, lineValueText):
    
    for i in range(sizeData):
        if serialComm and serialComm.rawData[i] is not None:  # Verifica si hay datos
            data[i].append(serialComm.rawData[i])
            lines[i].set_data(range(samples), data[i])
            lineValueText[i].set_text(f'signal {i} = {serialComm.rawData[i]}')

    if isCollect:
        collectData.append(copy.deepcopy(serialComm.rawData))
        labelData.append(float(entryLabel.get()))
        

# Configuración de la interfaz gráfica
root = Tk()
root.protocol('WM_DELETE_WINDOW', onClosing)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.grid(row=0, column=0, columnspan=5)

# Opción para seleccionar el puerto
port_var = StringVar(root)
port_var.set(list_ports()[0])  # Establecer el primer puerto como predeterminado

port_menu = OptionMenu(root, port_var, *list_ports())
port_menu.grid(row=1, column=1, padx=20, pady=20)

# Opción para seleccionar la tasa de baudios
baud_var = StringVar(root)
baud_options = [9600, 115200, 57600, 19200, 38400, 4800]  # Opciones comunes de baudios
baud_var.set(baud_options[1])  # Establecer 115200 como predeterminado

baud_menu = OptionMenu(root, baud_var, *baud_options)
baud_menu.grid(row=1, column=2, padx=20, pady=20)


# Botón para abrir la comunicación serial
open_port_button = Button(root, text='Abrir Puerto', command=open_serial_comm, font=16)
open_port_button.grid(row=1, column=4, padx=20, pady=20)

# Crear un frame para los controles
control_frame = Frame(root)
control_frame.grid(row=0, column=5, padx=20, pady=20)

# Etiqueta para el primer valor
entry_label = Label(control_frame, text='Clase')
entry_label.grid(row=0, column=0, padx=20, pady=10)

entry = Entry(control_frame, justify=LEFT)
entry.insert(END, '1')
entry.grid(row=1, column=0, padx=20, pady=10)

entry_label2 = Label(control_frame, text='Etiqueta')
entry_label2.grid(row=2, column=0, padx=20, pady=10)

entryLabel = Entry(control_frame, justify=LEFT)
entryLabel.insert(END, '0')
entryLabel.grid(row=3, column=0, padx=20, pady=10)

button1 = Button(control_frame, text='Iniciar', command=start, font=16)
button1.grid(row=4, column=0, padx=20, pady=10)

button2 = Button(control_frame, text='Pausar', command=pause, font=16)
button2.grid(row=5, column=0, padx=20, pady=10)

button3 = Button(control_frame, text='Borrar', command=delete, font=16)
button3.grid(row=6, column=0, padx=20, pady=10)

button4 = Button(control_frame, text='Guardar', command=save, font=16)
button4.grid(row=7, column=0, padx=20, pady=10)

# Crear widget de texto para mostrar mensajes
text_widget = Text(control_frame, height=10, width=50)
text_widget.grid(row=8, column=0, padx=20, pady=10)

anim = animation.FuncAnimation(fig, plotData, fargs=(lines, lineValueText), interval=sampleTime)

root.mainloop()
