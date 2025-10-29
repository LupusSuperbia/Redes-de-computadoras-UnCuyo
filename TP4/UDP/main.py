import socket
import threading
import time
from enum import Enum, auto


class ComandoUDP(Enum):
    EXIT = ('exit', 'desconectar', 'salir', 'quit')
'''
_create_udp_socket : 
- Se encarga de la configuracion del socket para poder ser usado tanto por el proceso que envia 
los datos al broadcast como el proceso que esta escuchando los datos que se estan enviando
al broadcast y al puerto, se utilizan funciones del import donde se setea las opciones
del socket, una es para donde va a mandar los mensajes que este seria el SO_BROADCAST 
y el otro es para que obtenga los paquetes y la direccion de donde la envian SO_REUSADDR
'''
class ClientUDP : 
    def __init__(self, port : int ):
        self.port = port 
        self.name = ''
        self.broadcast_ip = "255.255.255.255"
        self.socket_udp = self._create_udp_socket()
        self.running = True

    def _create_udp_socket(self):
        sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock_udp.bind(("", self.port)) 
        sock_udp.settimeout(1.0)
        return sock_udp


    def _set_name(self): 
        print("Ingresa tu nombre:")
        username = input()
        self.name = username

    def join_chat(self):
        join_message = f"El usuario {self.name} se ha unido al chat"
        self.socket_udp.sendto(join_message.encode(), (self.broadcast_ip, self.port))


    def leave_chat(self):
        leave_message = f"El usuario {self.name} ha abandonado el chat"
        self.socket_udp.sendto(leave_message.encode(), (self.broadcast_ip, self.port))

    def send_to_udp(self):
        self.join_chat()
        try : 
            while self.running : 
                msg = input("¬ ")
                message = f"El usuario {self.name} dice : {msg}"
                if msg.lower() in ComandoUDP.EXIT.value: 
                    self.func_error()
                    break
                self.socket_udp.sendto(message.encode(), (self.broadcast_ip, self.port))
        except ConnectionResetError as cr : 
            print('Se desconecto abrupatemente', e)
        except KeyboardInterrupt  as kr : 
            self.func_error()
            print("El cliente ha salido con el atajo de teclado CTRL-C ", kr)
        except EOFError as ef : 
            self.func_error()
            print("El usuario ha interrumpido la conexión CTRL-C el hilo ha detenido", ef)
        finally : 
            self.socket_udp.close()          
    
    def func_error(self):
        self.running = False
        self.leave_chat()

    def listen_udp(self):
        print("Escuchando  la LAN 49.44 : ")
        while self.running : 
            try :
                (data, (address, port)) = self.socket_udp.recvfrom(1024)
                print(f"{data.decode()} ({address}:{port})")
            except socket.timeout:
                continue
            except OSError:
                if not self.running:
                    break 
                else:
                    raise
if __name__ == "__main__" : 
    port = 60000
    client_udp = ClientUDP(port)
    client_udp._set_name()

    listen_thread = threading.Thread(target=client_udp.listen_udp, daemon=True)
    thread_send = threading.Thread(target=client_udp.send_to_udp, daemon=False)
    listen_thread.start()
    thread_send.start()
    try : 
        thread_send.join() 
    except KeyboardInterrupt as kr : 
        print("Se ha detenido el cliente UDP, ya no se puede recibir ni enviar mas datagramas", kr)
        pass
    print("El programa se cerro correctamente")