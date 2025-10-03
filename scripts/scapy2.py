from scapy.all import *
import time
import random

# Config: Ajusta a tu lab
IP_DESTINO = "10.65.1.150"  # Receptor
PUERTO_DESTINO = 60000
NUM_PAQUETES = 50  # Empieza bajo para no saturar
INTERVALO = 0.05   # Segundos entre paquetes (ajusta para más/menos interferencia)

def interferir():
    print(f"Iniciando interferencia UDP a {IP_DESTINO}:{PUERTO_DESTINO}...")
    for i in range(NUM_PAQUETES):
        # Payload aleatorio/molesto (ej. ruido en texto)
        payload_basura = f"*** INTERFERENCIA {random.randint(1,1000)} ***".encode()
        
        ip = IP(dst=IP_DESTINO)  # Sin spoof por ahora, para simplicidad
        udp = UDP(dport=PUERTO_DESTINO)
        pkt = ip / udp / Raw(load=payload_basura)
        
        send(pkt, verbose=0)
        print(f"Enviado paquete {i+1}: {payload_basura[:20].decode()}")
        time.sleep(INTERVALO) 
    print("Interferencia terminada. Verifica en el Receptor.")

if __name__ == "__main__":
    interferir()
