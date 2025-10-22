# INFORME TP3 - AGUSTÍN SAMPERI <br> - CAPA DE RED
## Actividad 1 
### Redes y Subredes : 
![redes_subredes](/home/ager1/Imágenes/Screenshots/redes-subredes.png)
#### **Configuracion Static** : 
- Router 1 : <br>
![router1](/home/ager1/Imágenes/Screenshots/router1.png)
- Router 2 : <br>
![router2](/home/ager1/Imágenes/Screenshots/router2.png)
- Router 3 : <br>  
![router3](/home/ager1/Imágenes/Screenshots/router3.png)
- Router 4 : <br>
![router4](/home/ager1/Imágenes/Screenshots/router4.png)
## **Actividad 2** 
### RIP : 
![RIP](/home/ager1/Imágenes/Screenshots/RIPRED.png)
- **Router 1 RIP** : 
![ROUTER1RIP](/home/ager1/Imágenes/Screenshots/router1-rip.png)
- **Router 2 RIP** : 
![Router2RIP](/home/ager1/Imágenes/Screenshots/router2-rip.png)

### **OSPF** : 
![OSPF](/home/ager1/Imágenes/Screenshots/OSPF.png)
- **ROUTER 1 OSPF** : 
![OSPFROUTER1](/home/ager1/Imágenes/Screenshots/OSPF-CONFIG-ROUTER1.png)
* **Show Config** : 
![OSPFshow](/home/ager1/Imágenes/Screenshots/routeconfigospf.png)
- **ROUTER 2 OSPF** : 
![OSPFROUTER2](/home/ager1/Imágenes/Screenshots/OSPF-CONFIG-ROUTER2.png)
* **Show Config** : 
![OSPFshow](/home/ager1/Imágenes/Screenshots/route2configospf.png)
## **Actividad 3** 
### www.google.com : 
![vtraceroutegoogle](/home/ager1/Imágenes/Screenshots/google.png)
terminal : 
![vtracerouteterminalgoogle](/home/ager1/Imágenes/Screenshots/google-traceroute.png)
### Hong Kong: 
![vtraceroutehongkong](/home/ager1/Imágenes/Screenshots/hongkong.png)
terminal : 
![vtracerouteterminalhongkong](/home/ager1/Imágenes/Screenshots/hongkong-terminal.png)
### Nepal: 
![vtraceroutenapal](/home/ager1/Imágenes/Screenshots/nepal.png)
terminal : 
![vtracerouteterminalgoogle](/home/ager1/Imágenes/Screenshots/nepal-terminal.png)
### Lujan de Cuyo: 
![vtraceroutelujandecuyo](/home/ager1/Imágenes/Screenshots/lujandecuyo.png)
terminal : 
![vtracerouteterminallujandecuyo](/home/ager1/Imágenes/Screenshots/lujandecuyoterminal.png)
### LocalHost: 
![vtraceroutelocalhost](/home/ager1/Imágenes/Screenshots/localhost.png)
terminal : 
![vtracerouteterminalgoogle](/home/ager1/Imágenes/Screenshots/localhost-terminal.png)
## **Actividad 4**
### ***4.1*** : 

***Router :*** 

![router](/home/ager1/Imágenes/Screenshots/router.png)

 *¿La dirección IP origen de un paquete que entra a un router cambia al salir el
paquete del router? 
No, la dirección de IP origen no es afectada cuando 
el paquete sale del router, el router solo usa 
las direcciones ip para elegir el camino. utiliza el FIB, para reenviar el paquete por la interfaz correspondiente 
* ¿La dirección Ethernet origen de un paquete que entra a un
router cambia al salir el paquete del router ? : 
La dirección Ethernet (MAC) de origen cambia al salir de un router, esto pasa porque las MAC identifican los dispositivos dentro de un mismo enlace fisico, 
y el cual no es el destino final. Entonces el router se encarga de eliminar la trama de entrada y crear una nueva,
agregando su propia MAC de salida y la del siguiente salto. 
La IP permanece igual porque la ip sería como la dirección de una casa, mientras la MAC sería la etiqueta postal temporal del camion de transporte de la zona, 
cada vez que llega a un nueva postal, se le cambia la etiqueta postal (MAC)

***Switch:***

![switch](/home/ager1/Imágenes/Screenshots/switch.png)
* ¿La dirección IP de un paquete que entra a un switch cambia al salir el paquete
del switch? : 
El switch no trabaja en Capa 3 es decir no revisa ni modifica la dirección IP. 
El paquete esta encapsulado dentro de la tramma (que contiene la MAC) y la trama se reenvia intacta, opera en Capa 2 (MODELO OSI), el cual se encarga de manejar las direcciones, examina la dirección MAC de destino para reenviar la trama al puerto correcto.   
* La dirección Ethernet de un paquete que entra a un switch cambia
al salir el paquete del switch? : 
No, la direccion Ethernet (MAC), no cambia al salir del switch, lo que hace el switch es copiar el frame y lo pasa al siguiente puerto, es decir lo reenvia utilizando el puerto de salida apropiado basandose en su tabla de direcciones MAC (O TABLA CAM)

## ***ACTIVIDAD 4.2*** 

*  Si un paquete se envía de una computadora en una red a otra computadora en
la misma red, ¿Pasa el paquete por el router?.: 
No, el paquete no pasa por el router si la computadora de origen y la de destino se encuentran en la misma red, (o subred) lógica, pero cómo funciona esto ? 
Juega un papel muy importante la tarjeta de red y la mascara de subred, ya que cuando una computadora host A quiere enviar un paquete ip a otra computadora (Host B), el host A compara la direccion ip de destino con su propia direccion IP utilizando su mascara de subred, si esta comparacion de como resultado de que ambas IPs pertenecen a la misma subred el HostA sabe que el destino es el host local, y por lo tanto no necesita recurrir al router 
Acá el switch tambien tiene un rol importante ya que cuando el host A envia una solicitud ARP broadcast preguntando quien tiene la ip del HOST B y que le responda con su MAC
El switch se encarga de recibir esta trama broadcast y la reenvia a todos los puertos, excepto al HOST A, el Host B responde directamente al HOST A con su MAC
Una vez el HOST A tiene la MAC de destino, el switch recibe las tramas posteriores y las conmuta (envia) directamente al puerto donde el HOST B esta conectado, esto lo hace basandose en su tabla MAC/CAM
* Si un paquete se envía de una computadora en una red a otra computadora en
otra red ¿Pasa el paquete por el router?
Si, pasa por el router ya que primero el host A analiza si esta pertence al host local, si no es asi lo manda al router (la puerta de enlace predeterminada), el router busca en las tablas de enrutamienot (rutas estatics, dinamicas o directamente conectadas) para ver donde esta el siguiente salto que conecta con la red solicitada, le avisa al host a que puede mandar los paquetes porque tiene la conmutacion para poder enviar estos paquetes. 
*¿Qué información indica a la computadora origen si la IP destino está en la
misma red (y puede enviarle paquetes directamente) o en una red diferente (y
debe enviar el paquete al router)?

