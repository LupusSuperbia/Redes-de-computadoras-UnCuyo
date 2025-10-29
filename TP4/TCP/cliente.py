import socket 
import threading
from Comandos import ServerCommand, loading, clear_term


class ClienteTCP : 
    def __init__ (self, host : str , port : int): 
        self.host = host 
        self.port = port 
        self.running = True 
        self.client_socket = self.connect_socket() 
    def connect_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.host, self.port))
        return client_socket



    def send_msg(self):
        try : 
            while self.running : 
                msg = input("#")
                msg_complete = msg.encode()
                if msg.lower() in ServerCommand.EXIT.value: 
                    print(f"Te has desconectado")
                    self.client_socket.send(msg_complete)
                    self.running = False
                    if hasattr(self, 'client_socket'): 
                        self.client_socket.close()
                    break
                self.client_socket.send(msg_complete)
        except OSError as e: 
            if self.running == False : 
                print("La conexión se ha cerrado")
            else : 
                print(f'Error de conexión {e}')          
        except Exception as e : 
            print(e)
        finally :  
            self.client_socket.close()
    def listen_server(self): 
        try : 
            while self.running : 
                data = self.client_socket.recv(1024)
                if not data:  # Servidor desconectado
                     print("El servidor se ha desconectado.")
                     break
                print(data.decode('utf-8'))
        except OSError as e : 
            print(e)
        except  Exception as e : 
            print(e)
        finally :
            
            self.running = False
            pass



if __name__ == "__main__":
    #loading() 

    host = input("Ingrese el host del servidor:") 
    while True :  
        port_str = input("Ingrese el puerto : ")
        try : 
            port = int(port_str)
            break
        except Exception as e : 
            print(f'El puerto tiene que ser un numero {e}')

    cliente_socket = ClienteTCP(host, port)
    send_message = threading.Thread(target=cliente_socket.send_msg)
    listen_server = threading.Thread(target=cliente_socket.listen_server, daemon=True)
    send_message.start()
    listen_server.start()