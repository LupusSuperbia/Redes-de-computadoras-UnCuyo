from enum import Enum, auto
import os 
import time
class ServerCommand(Enum):
    LIST_CLIENTS = ('/clients',)
    EXIT = ("/exit", 'desconectar', "/quit", 'quit', 'salir', "/salir")
    CLEAR = ('/clear',)
   # SERVER_SHUTDOWN = auto()
    STOP = ('salir', 'quit', 'exit', 'desconectar')
def loading(): 
    string = "="
    for i in range(0,50):
        clear_term()
        percentage = (i + 1) * 2
        print(f"Iniciando Servidor EPICARDIUM... {percentage}%")
        print(f"{string} {'.' * (50 - len(string))}")
        string = string + "="
        time.sleep(0.03)  # import time
    clear_term()

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')
