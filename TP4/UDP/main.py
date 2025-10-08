import socket
import threading

BROADCAST_IP = "255.255.255.255"
PORT = 60000
def _create_udp_socket(bind=False):
    sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if bind : 
        sock_udp.bind(('', PORT))
    return sock_udp


def _set_name(): 
    print("Ingresa tu nombre:\n")
    username = input()
    return username 

def join_chat(name, sock):
    join_message = f"El usuario {name} se ha unido al chat"
    sock.sendto(join_message.encode(), (BROADCAST_IP, PORT))


def leave_chat(name, sock):
    leave_message = f"El usuario {name} ha abandonado el chat"
    sock.sendto(leave_message.encode(), (BROADCAST_IP, PORT))

def send_to_udp(name):
    sock = _create_udp_socket()
    join_chat(name, sock)
    try : 
        while True : 
            msg = input("¬ ")
            message = f"El usuario [{name}] dice  : {msg}"
            sock.sendto(message.encode(), (BROADCAST_IP, PORT))
            if msg.lower() == "exit": 
                leave_chat(name, sock)
                break
    finally : 
        sock.close()            
def listen_udp():
    sock = _create_udp_socket(bind=True)
    print("Escuchando  la LAN 49.44 : ")
    while True : 
        data, addr = sock.recvfrom(1024)
        print(f"{data.decode()} ({addr[0]})")

if __name__ == "__main__" : 
    name = _set_name()
    threading.Thread(target=listen_udp, daemon=True).start()
    send_to_udp(name)