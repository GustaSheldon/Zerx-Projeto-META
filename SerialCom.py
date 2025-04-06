import serial.tools.list_ports
import time

# Lista as portas COM disponíveis
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

# Solicita ao usuário que selecione a porta COM
com = input("Selecione a porta COM do Arduino: ")

# Verifica se a porta COM selecionada existe
use = None
for i in range(len(portsList)):
    if portsList[i].startswith("COM" + str(com)):
        use = "COM" + str(com)
        print("Conectado à porta:", use)
        break

# Se a porta COM não for encontrada, encerra o programa
if not use:
    print("Porta COM não encontrada.")

# Configura a porta serial
serialInst.baudrate = 9600
serialInst.port = use
serialInst.open()

def execute(command):
    serialInst.write((command + '\n').encode('utf-8'))  # Envia o comando
    print(command)