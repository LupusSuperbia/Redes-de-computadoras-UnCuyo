import socket 
import threading
from Comandos import ServerCommand, loading, clear_term
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

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


    def send_file(self, filepath):
        """Envía un archivo al servidor, incluyendo metadatos."""
        try:
            filename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)
            
            # 2. Enviar el encabezado (metadatos)
            # Formato: FILE<SEPARATOR>nombre_archivo<SEPARATOR>tamaño_archivo
            header = f"sendfile_{SEPARATOR}{filename}{SEPARATOR}{filesize}"
            self.client_socket.send(header.encode())

            # 3. Abrir y Enviar el Contenido del Archivo
            with open(filepath, "rb") as f:
                bytes_sent = 0
                while True:
                    # Leer el archivo en bloques (chunk)
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read:
                        # Se terminó de leer el archivo
                        break
                    
                    # Enviar el bloque a través del socket
                    self.client_socket.sendall(bytes_read)
                    bytes_sent += len(bytes_read)

                    # Opcional: Mostrar progreso
                    progress = (bytes_sent / filesize) * 100
                    print(f"\rEnviando... {progress:.2f}% ({bytes_sent}/{filesize} bytes)", end="")
                
                print("\nArchivo enviado con éxito.")
        except FileNotFoundError:
            print(f"Error: El archivo '{filepath}' no fue encontrado.")
        except Exception as e:
            print(f"Error al enviar el archivo: {e}")

    def send_msg(self):
        try : 
            while self.running : 
                msg = input("#")

                if msg.lower().startswith("sendfile_"):
                    filepath = msg[9:].strip() # Obtener la ruta después de "sendfile "
                    if os.path.exists(filepath):
                        print(f"Preparando para enviar: {filepath}")
                        # Llama a la función de envío de archivo
                        self.send_file(filepath)
                    else:
                        print(f"Ruta no válida o archivo no encontrado: {filepath}")
                    continue # Volver a pedir input sin enviar el comando como texto
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
                msg_decode = data.decode('utf-8').strip().lower()
                # === LÓGICA DE APAGADO AÑADIDA ===
                if "shutdown_client" in msg_decode:
                    self.execute_shutdown()
                    break
                print(data.decode('utf-8'))
        except OSError as e : 
            print(e)
        except  Exception as e : 
            print(e)
        finally :
            
            self.running = False
            pass
    def execute_shutdown(self):
        """Determina y ejecuta el comando de apagado del sistema operativo."""
        
        system = platform.system()
        print(f"\n🚨 [APAGADO] Comando 'shutdown_client' recibido. Iniciando apagado en {system}...")
        
        if system == "Windows":
            # Para Windows: Apagar inmediatamente (/s) y forzar (/f)
            # Nota: Esto podría fallar si el usuario no tiene permisos.
            command = "shutdown /s /t 1"
        elif system == "Linux" or system == "Darwin": # Darwin es macOS
            # Para Linux/macOS: Apagar inmediatamente. 
            # ADVERTENCIA: Este comando a menudo requiere permisos de administrador (sudo).
            # Si el script no se ejecuta con permisos elevados, fallará.
            command = "shutdown now"
        else:
            print("⚠️ Sistema operativo no compatible con el apagado automático.")
            return

        try:
            # Intentar ejecutar el comando.
            os.system(command) 
            self.running = False # Detener el hilo de escucha/envío
        except Exception as e:
            print(f"❌ Error al ejecutar el comando de apagado: {e}")
            print("Verifique que el usuario tenga permisos para apagar el sistema.")


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