
import socket 
import threading 
import os 
import time
from Comandos import ServerCommand

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE= 4096 
FILE_DESTINATION_FOLDER = "/home/ageri/Documents" # Carpeta donde se guardarán los archivos


class ServerTCP: 
    
    def __init__(self, host, port, listen): 
        self.port = port 
        self.host = host 
        self.listen = listen #Cuantas conexiones va a permitir el servidor al mismo momento
        self.clients_connected = {} ## Diccionario (Parecido a una tabla hash para mantener los datos de los clientes conectados)
        self.lock = threading.Lock() ## Este metodo de threading funciona para que haya problemas con la condicion de carrera, es mas a nivel de concurrencia cuando vemos la lista de los clientes conectados
        self.running = True  ##Flag que nos permite detener el server en algun momento dado 
        self.server_socket = self._create_tcp_socket() ## Directamente llamamos al metodo para crear el socket desde el init, asi podemos tener una instancia del server como atributo de nuestra clase, y nos permite el llamado en distintas partes del codigo

    def _create_tcp_socket(self) :
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            server_socket.bind((self.host, self.port))
            server_socket.listen(self.listen)
        except Exception as e:
            print("Error:", e) 
        return server_socket 
        
    def _mainloop_server(self): 
        print("#################### BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM ################")
        try :  
            while self.running : 
                (client_socket, address) = self.server_socket.accept()
                thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
                thread.start()
        except OSError as o : 
            print("Se cerro abruptamente le servidor")
        except Exception as e : 
            print("Error: ", e)
        finally : 
            self.server_socket.close() 
    

    def handle_client(self, client_socket, client_address):
        try: 
            client_socket.send(("💬Ingresa tu nombre :").encode())
            data = client_socket.recv(1024)
            client_name = data.decode().strip()
            welcome_to_chat = f"=============== BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM {client_name}     ==================="
            client_socket.send(welcome_to_chat.encode())
            with self.lock : 
                self.clients_connected[client_address] = {'socket' : client_socket, 'name' : client_name }
            self.send_message(f"👋 Se ha conectado el cliente : {client_name}", client_address)
            while True : 
                data = client_socket.recv(BUFFER_SIZE)
                if not data : 
                    break
                try:
                    msg_decode = data.decode().strip()
                except UnicodeDecodeError:
                    # Si no es texto válido, podría ser un error o el inicio de datos binarios
                    # sin un encabezado, lo trataremos como un error por ahora.
                    print(f"[{client_name}]: Mensaje recibido no es texto. Ignorando.")
                    continue
                    
                # 2. Verificar si es un comando de envío de archivo
                if msg_decode.startswith(f"sendfile_{SEPARATOR}"):
                    # El cliente está enviando un archivo.
                    try:
                        # Extraer metadatos
                        parts = msg_decode.split(SEPARATOR)
                        
                        # Esperamos 3 partes: [0]=FILE, [1]=filename, [2]=filesize
                        if len(parts) == 3 and parts[0] == "sendfile_":
                            filename = parts[1]
                            filesize = int(parts[2])
                            
                            print(f"\n[INFO] {client_name} intenta enviar archivo: '{filename}' ({filesize} bytes)")
                            
                            # Informar a otros clientes
                            self.send_message(f"📢 {client_name} está enviando el archivo '{filename}'.", client_address)

                            # Llama a la nueva función de recepción
                            success = self._receive_file(client_socket, filename, filesize)
                            
                            if success:
                                self.send_message(f"🎉 {client_name} ha enviado el archivo '{filename}' con éxito.", client_address)
                            else:
                                self.send_message(f"❌ Falló la recepción del archivo '{filename}' de {client_name}.", client_address)
                                
                            # Después de recibir el archivo, volvemos al inicio del bucle
                            continue 
                            
                        else:
                            print(f"[ERROR]: Formato de encabezado de archivo inválido de {client_name}")
                            
                    except ValueError:
                        print(f"[ERROR]: Tamaño de archivo no es un número válido de {client_name}")
                    except Exception as e:
                        print(f"[ERROR] durante el manejo del encabezado de archivo: {e}")
                msg_decode = data.decode()
                if msg_decode.lower() in ServerCommand.EXIT.value  :
                    
                    print(f'RECIBIDO EL CLIENTE {self.clients_connected[client_address]['name']} SE HA DESCONECTADO ')
                    msg = f"SE HA DESCONECTADO UN CLIENTE {self.clients_connected[client_address]['name']} 🏃‍♂️"
                    self.send_message(msg, client_address)

                    break
                print(f"Cliente  {client_name} : {msg_decode}")
                what_to_send = f"{client_name} : {msg_decode}"
                #client_socket.send(what_to_send.encode('utf-8'))
                self.send_message(what_to_send, client_address)
        except ConnectionResetError as cr : 
            print(f'El cliente {client_name} ha cerrado abruptamente 🔥')
        except Exception as e : 
            print("Se ha producido un error :", e)
        finally : 
            with self.lock : 
                if client_address in self.clients_connected: 
                    self.clients_connected.pop(client_address)
            client_socket.close()
            print(f'Conexión con {client_name} terminada')
    


    def _receive_file(self, client_socket, filename, filesize):
        """Maneja la recepción de datos binarios del archivo."""
        
        # 1. Crear la carpeta de destino si no existe
        if not os.path.exists(FILE_DESTINATION_FOLDER):
            os.makedirs(FILE_DESTINATION_FOLDER)
            
        filepath = os.path.join(FILE_DESTINATION_FOLDER, filename)
        
        try:
            # 2. Abrir el archivo de destino en modo escritura binaria
            with open(filepath, "wb") as f:
                bytes_received = 0
                
                # Bucle de recepción: se ejecuta hasta que se reciben todos los bytes (filesize)
                while bytes_received < filesize:
                    # Calcular cuántos bytes quedan por recibir
                    bytes_to_receive = filesize - bytes_received
                    
                    # Recibir solo un bloque (BUFFER_SIZE) o lo que queda, lo que sea menor
                    data = client_socket.recv(min(BUFFER_SIZE, bytes_to_receive))
                    
                    if not data:
                        # La conexión se cerró inesperadamente
                        print(f"\nError: Conexión cerrada antes de completar el archivo.")
                        return False

                    # Escribir los bytes recibidos en el archivo
                    f.write(data)
                    bytes_received += len(data)
                    
                    # Opcional: Mostrar progreso en el servidor
                    progress = (bytes_received / filesize) * 100
                    print(f"\rRecibiendo {filename}... {progress:.2f}% ({bytes_received}/{filesize} bytes)", end="")

                print(f"\n✅ Archivo '{filename}' recibido con éxito y guardado en: {filepath}")
                return True
                
        except Exception as e:
            print(f"Error durante la recepción/escritura del archivo: {e}")
            return False
    
    def send_message(self, msg, client_address):
        with self.lock : 
            try : 
                clients = self.clients_connected
                if not clients: 
                        return 
                buff_entry_encode = msg.encode()
                for address, client in clients.items() :
                    if address != client_address : 
                        client['socket'].send(buff_entry_encode)
            except Exception as e : 
                print("No se pudo mandar mensaje",)

    def send_message_server(self):
        
            while True : 
                try:
                    buff = input("#").lower()
                    if buff in ServerCommand.STOP.value:
                        if self.disconnect_server(): 
                            break
                        else : 
                            continue
                    elif buff in ServerCommand.LIST_CLIENTS.value : 
                        self.list_clients()
                        continue
                    self.send_message_clients(buff)
                except OSError as o : 
                    print("ERROR : ", o)
                except KeyboardInterrupt as e : 
                    print('Se ha interrupido el servicio con CTRL-C')
                    if self.verify_clients() :
                        print('No hay clientes, se puede esconectar el servidor')
                    
                    else : 
                        print('Hay clientes conectados al servidor, no se puede desconectar')
                        self.list_clients()
                         
                except Exception as e:
                    print("Error en send message server:", e) 
                finally :
                    pass
       
            
    def list_clients(self):
        with self.lock: 
            print('====== CLIENTES CONECTADOS ==== ')
            for clients in self.clients_connected.values():
                    print(clients['name'])
    def verify_clients(self):
        with self.lock : 
           return not bool(self.clients_connected)
            
    def disconnect_server(self)  :
        if self.verify_clients(): 
            buff = "El servidor se ha desconectado"
            print(buff)
            self.running = False
            if hasattr(self, 'server_socket'): 
                self.server_socket.close()
            return True 
        else : 
            print("No se puede desconectar el servidor, ya que posee clientes conectados")
            self.list_clients()
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



if __name__ == "__main__":
    #loading()
    server = ServerTCP('0.0.0.0', 50000, listen=5)
    server_thread = threading.Thread(target=server._mainloop_server)
    server_thread.start()
    send = threading.Thread(target=server.send_message_server, daemon=True)
    send.start()
