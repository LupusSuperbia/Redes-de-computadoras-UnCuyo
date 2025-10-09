# 1. Importar los módulos necesarios
#    - Usar el módulo 'socket' para manejar conexiones de red
#    - Opcionalmente, usar 'threading' si se desea manejar múltiples clientes simultáneamente
import socket 
import threading 

# 2. Definir las constantes del servidor
#    - Especificar la dirección IP del host (por ejemplo, 'localhost' o '127.0.0.1' para local)
#    - Elegir un número de puerto (por ejemplo, 12345, asegurarse que esté libre)
IP_HOST = 'localhost'
PORT = 60000
# 3. Crear un objeto socket
#    - Usar socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#    - AF_INET para IPv4, SOCK_STREAM para TCP
# 4. Vincular el socket al host y puerto
#    - Usar el método .bind((host, puerto))
#    - Asegurarse de manejar posibles excepciones (por ejemplo, puerto en uso)
def _create_tpc_socket() :
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try : 
        socket_tcp.bind(IP_HOST, PORT)
        socket_tcp.listen(5)
    except Exception as e:
        raise e
    return socket_tcp 

def _mainloop_server(): 
    socket_server = _create_tpc_socket() 
    while True : 
        (socket_client, address) = socket_server.accept()
        


# 5. Configurar el servidor para escuchar conexiones
#    - Usar el método .listen() para permitir conexiones entrantes
#    - Especificar el número máximo de conexiones en cola (por ejemplo, 5)

# 6. Crear un bucle principal para aceptar conexiones
#    - Usar el método .accept() para esperar conexiones de clientes
#    - Este método devuelve un nuevo socket para el cliente y su dirección
# 7. Manejar la comunicación con el cliente
#    - Usar el socket del cliente para recibir datos con .recv(tamaño_buffer)
#    - Decodificar los datos recibidos si es necesario (por ejemplo, de bytes a string)
#    - Procesar los datos según la lógica del servidor
#    - Enviar respuestas al cliente usando .send() o .sendall()

# 8. (Opcional) Implementar manejo de múltiples clientes
#    - Usar hilos (threading) o procesos para manejar cada cliente en paralelo
#    - Crear una función para manejar la comunicación con cada cliente
#    - Iniciar un nuevo hilo/proceso por cada conexión aceptada

# 9. Manejar excepciones y cierres
#    - Incluir manejo de errores para conexiones fallidas o desconexiones
#    - Cerrar los sockets de los clientes con .close() cuando terminen
#    - Cerrar el socket del servidor al finalizar el programa

# 10. (Opcional) Agregar un mecanismo de salida
#    - Implementar una forma de detener el servidor (por ejemplo, con un comando específico)
#    - Asegurarse de cerrar todas las conexiones abiertas antes de salir