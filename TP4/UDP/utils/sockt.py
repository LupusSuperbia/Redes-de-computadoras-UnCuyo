import socket as skt
import threading
from enum import Enum

class Protocol(Enum):
    TCP = "tcp"
    UDP = "udp"

class BaseSocket: 
    def __init__(self, host : str, port : str):
        self.host = host 
        self.port = port 
        self.sock = None 

    def start(self):
        raise NotImplementedError

class TCPSocket(BaseSocket) : 
    def start(self):
        self.sock = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        pass