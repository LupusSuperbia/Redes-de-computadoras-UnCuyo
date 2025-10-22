
import socket 
import threading 
import os 
import time
from enum import Enum, auto
class ServerCommand(Enum):
    LIST_CLIENTS = '/clients'
    EXIT = "/exit"
    
   # SERVER_SHUTDOWN = auto()

class ServerTCP: 
    

    def __init__(self, host, port, listen): 
        self.port = port 
        self.host = host 
        self.listen = listen
        self.clients_connected = {}
        self.lock = threading.Lock()
        self.running = True 
        self.server_socket = self._create_tcp_socket()

    def _create_tcp_socket(self) :
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.listen)
        except Exception as e:
            raise e
        return server_socket 
        
    def _mainloop_server(self): 
        print("#################### BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM ################")
        try :  
            while self.running : 
                (client_socket, address) = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()
        except Exception as e : 
            print("Error: ", e)
        finally : 
            self.server_socket.close() 
    

    def handle_client(self, client_socket, client_address):
        try: 
            client_socket.send(("💬Ingresa tu nombre :").encode())
            data = client_socket.recv(1024)
            client_name = data.decode().strip()
            welcome_to_chat = f"#################### BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM {client_name} ################"
            print(welcome_to_chat)
            client_socket.send(welcome_to_chat.encode())
            with self.lock : 
                self.clients_connected[client_address] = {'socket' : client_socket, 'name' : client_name }
            self.send_message(f"👋 Se ha conectado el cliente : {client_name}", client_address)
            while True : 
                data = client_socket.recv(1024)
                if not data : 
                    break
                msg_decode = data.decode()
                if msg_decode.lower().find('/') != -1  :
                    
                    print(f'RECIBIDO EL CLIENTE {self.clients_connected[client_address]['name']} SE HA DESCONECTADO ')
                    msg = f"SE HA DESCONECTADO UN CLIENTE {self.clients_connected[client_address]['name']} 🏃‍♂️"
                    self.send_message(msg, client_address)

                    break
                print(f"Cliente  {client_name} : {msg_decode}")
                what_to_send = f"{client_name} : {msg_decode}"
                #client_socket.send(what_to_send.encode('utf-8'))
                self.send_message(what_to_send, client_address)
        except Exception as e : 
            print("Se ha producido un error :", e)
        finally : 
            with self.lock : 
                if client_address in self.clients_connected: 
                    self.clients_connected.pop(client_address)
            client_socket.close()
            print(f'Conexión con {client_name} terminada')
        
    def send_message(self, msg, client_address):
        with self.lock : 
            clients = self.clients_connected
            if not clients: 
                    return 
            buff_entry_encode = msg.encode()
            for address, client in clients.items() :
                if address != client_address : 
                    client['socket'].send(buff_entry_encode)

    def send_message_server(self):
        try:
            while True : 
                buff = input("#")
                if buff.lower() in ['exit', 'salir', 'quit']:
                  if self.disconnect_server(): 
                    break
                  else : 
                    print('No se puede desconectar')  
                    continue
                self.send_message_clients(buff)
        except KeyboardInterrupt as e : 
            print('Se ha interrupido el servicio con CTRL-C')
            if self.verify_clients() :
                print('No hay clientes, se puede esconectar el servidor')
                return
            else : 
                print('Hay clientes conectados al servidor, no se puede desconectar')
                return 
        except Exception as e:
            raise e
        finally :
            return
            

    def verify_clients(self):
        with self.lock : 
           return not bool(self.clients_connected)
            
    def disconnect_server(self)  :
        if self.verify_clients(): 
            buff = "El servidor se ha desconectado"
            print(buff)
            self.send_message_clients(buff)
            self.running = False

            if hasattr(self, 'server_socket'): 
                self.server_socket.close()
            return True 
        else : 
            print("No se puede desconectar el servidor, ya que posee clientes conectados")
            return False 
            
    def send_message_clients(self, msg):
        with self.lock : 
            clients = self.clients_connected
            if not clients: 
                return 
            buff_entry = f"Server : {msg}"
            buff_entry_encode = buff_entry.encode()
            for client in self.clients_connected.values() : 
                client['socket'].send(buff_entry_encode)

def loading(): 
    string = "#"
    for i in range(0,50):
        clear_term()
        percentage = (i + 1) * 2
        print(f"Iniciando Servidor EPICARDIUM... {percentage}%")
        print(f"{string} {'.' * (50 - len(string))}")
        string = string + "#"
        time.sleep(0.03)  # import time
    clear_term()

def clear_term():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    #loading()
    server = ServerTCP('0.0.0.0', 50000, listen=5)
    server_thread = threading.Thread(target=server._mainloop_server)
    server_thread.start()
    send = threading.Thread(target=server.send_message_server, daemon=True)
    send.start()
