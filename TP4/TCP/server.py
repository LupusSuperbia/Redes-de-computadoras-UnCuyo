
import socket 
import threading 
import os 
import time

IP_HOST = '0.0.0.0'
PORT = 60000
clients_connected = {}

def _create_tcp_socket() :
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try : 
        socket_tcp.bind((IP_HOST, PORT))
        socket_tcp.listen(5)
    except Exception as e:
        raise e
    return socket_tcp 

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




def _mainloop_server(): 
    socket_server = _create_tcp_socket()
    print("#################### BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM ################")
    try :  
        while True : 
            (socket_client, address) = socket_server.accept()
            clients_connected[address] = socket_client
            thread = threading.Thread(target=handle_client, args=(socket_client, address))
            thread.start()
    except Exception as e : 
        raise e
    finally : 
        socket_server.close() 

def handle_client(client_socket, client_address):
    try: 
        data = client_socket.recv(1024)
        welcome_to_chat = f"#################### BIENVENIDOS A LA SALA DE CHAT MAS EPICARDIUM {data.decode()} ################"
        client_socket.send(welcome_to_chat.encode())
        print(f"Se ha conectado el cliente : {data.decode()}")
        while True : 
            data = client_socket.recv(1024)
            if not data : 
                break
            if data.decode('utf-8').lower().find('desconectar') != -1  :
                print(f'RECIBIDO EL CLIENTE {client_address[1]} SE HA DESCONECTADO')
                msg = f"SE HA DESCONECTADO UN CLIENTE {client_address[1]}"
                send_message_clients(clients_connected, msg)
                clients_connected.pop(client_address)
                break
            print(f"Recibido de {data.decode('utf-8')}")
            what_to_send = f"{client_address[1]} {data.decode('utf-8')}"
            client_socket.send(what_to_send.encode('utf-8'))
            send_mensage(clients_connected, what_to_send, client_address)
    except Exception as e : 
        raise e
    finally : 
        client_socket.close()

def send_mensage(clients, msg, client_address):
    if not clients: 
            return 
    buff_entry_encode = msg.encode()
    for address, sock in clients.items() :
        if address != client_address : 
            sock.send(buff_entry_encode)

def send_mensage_server(clients):
    try:
        while True : 
            buff = input("#")
            if buff.lower() in ['exit', 'salir', 'quit']:
                if verify_clients(clients): 
                    buff = "El servidor se ha desconectado"
                    print(buff)
                    send_message_clients(clients, buff)
                    break
                else : 
                    print("No se puede desconectar el servidor, ya que posee clientes conectados")
            send_message_clients(clients, buff)
    except Exception as e:
        raise e
    finally :
        verify_clients(clients)

def verify_clients(clients):
    if not clients : 
         return True 
    else : 
        return False
        

def send_message_clients(clients, msg):
    if not clients: 
        return 
    buff_entry = f"Server : {msg}"
    buff_entry_encode = buff_entry.encode()
    for client in clients.values() : 
        client.send(buff_entry_encode)

if __name__ == "__main__":
    #loading()
    server_thread = threading.Thread(target=_mainloop_server)
    server_thread.start()
    send = threading.Thread(target=send_mensage_server, args=(clients_connected, ), daemon=True)
    send.start()
