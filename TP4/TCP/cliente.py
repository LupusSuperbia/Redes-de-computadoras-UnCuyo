import socket 
import threading


def connect_socket(host : str, port : int):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    return client_socket

def send_msg_join(client_socket, name):
    try :   
            msg_complete = f"{name} "
            client_socket.send(msg_complete.encode())
    except Exception as e : 
        print(e)


def send_msg(client_socket):
    try : 
        while True : 
            msg = input("#")
            if msg.lower() == 'desconectar': 
                print(f"te has desconectado")
               
                break
            msg_complete = msg.encode()
            client_socket.send(msg_complete)
    except Exception as e : 
        print(e)
    finally : 
        client_socket.close()
def listen_server(client_socket):
    try : 
        while True : 
            data = client_socket.recv(1024)
            # if not data:  # Servidor desconectado
            #     print("El servidor se ha desconectado.")
            #     break
            print(data.decode('utf-8'))
    except  Exception as e : 
        print(e)
    finally : 
        client_socket.close()

if __name__ == "__main__":
    client_socket = connect_socket('127.0.0.1', 50000)
    send= threading.Thread(target=send_msg, args=(client_socket,))
    send.start()
    listen = threading.Thread(target=listen_server, args=(client_socket, ), daemon=True)
    listen.start()