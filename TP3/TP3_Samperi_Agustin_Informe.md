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
### ***Activdad 4.1 Diferencias entre paquetes IP y tramas Ethernet*** : 

***Router :*** 

![router](/home/ager1/Imágenes/Screenshots/router.png)

 ***¿La dirección IP origen de un paquete que entra a un router cambia al salir el**
**paquete del router?** 
No, la dirección de IP origen no es afectada cuando 
el paquete sale del router, el router solo usa 
las direcciones ip para elegir el camino. utiliza el FIB, para reenviar el paquete por la interfaz correspondiente 
* **¿La dirección Ethernet origen de un paquete que entra a un**
**router cambia al salir el paquete del router ? :** 
La dirección Ethernet (MAC) de origen cambia al salir de un router, esto pasa porque las MAC identifican los dispositivos dentro de un mismo enlace fisico, 
y el cual no es el destino final. Entonces el router se encarga de eliminar la trama de entrada y crear una nueva,
agregando su propia MAC de salida y la del siguiente salto. 
La IP permanece igual porque la ip sería como la dirección de una casa, mientras la MAC sería la etiqueta postal temporal del camión que hace transporte en la zona, 
cada vez que llega a un nueva postal, se le cambia la etiqueta postal (MAC)

***Switch:***

![switch](/home/ager1/Imágenes/Screenshots/switch.png)
* **¿La dirección IP de un paquete que entra a un switch cambia al salir el paquete
del switch? :** 
El switch no trabaja en Capa 3 es decir no revisa ni modifica la dirección IP. 
El paquete esta encapsulado dentro de la trama (que contiene la MAC) y la trama se reenvía intacta, opera en Capa 2 (MODELO OSI), el cual se encarga de manejar las direcciones, examina la dirección MAC de destino para reenviar la trama al puerto correcto.   
* **La dirección Ethernet de un paquete que entra a un switch cambia**
**al salir el paquete del switch? :** 
No, la dirección Ethernet (MAC), no cambia al salir del switch, lo que hace el switch es copiar el frame y lo pasa al siguiente puerto, es decir lo reenvía utilizando el puerto de salida apropiado basándose en su tabla de direcciones MAC (O TABLA CAM)

## ***ACTIVIDAD 4.2 - Configuración de red de cada computadora*** 

*  **Si un paquete se envía de una computadora en una red a otra computadora en**
**la misma red, ¿Pasa el paquete por el router?.**: 
No, el paquete no pasa por el router si la computadora de origen y la de destino se encuentran en la misma red, (o subred) lógica, pero cómo funciona esto ? 
Juega un papel muy importante la tarjeta de red y la mascara de subred, ya que cuando una computadora host A quiere enviar un paquete ip a otra computadora (Host B), el host A compara la dirección IP de destino con su propia dirección IP utilizando su mascara de subred, si esta comparación de como resultado de que ambas IPs pertenecen a la misma subred el HostA sabe que el destino es el host local, y por lo tanto no necesita recurrir al router 
Acá el switch también tiene un rol importante ya que cuando el host A envía una solicitud ARP broadcast preguntando quien tiene la ip del HOST B y que le responda con su MAC
El switch se encarga de recibir esta trama broadcast y la reenvía a todos los puertos, excepto al HOST A, el Host B responde directamente al HOST A con su MAC
Una vez el HOST A tiene la MAC de destino, el switch recibe las tramas posteriores y las conmuta (envía) directamente al puerto donde el HOST B esta conectado, esto lo hace basándose en su tabla MAC/CAM
* Si un paquete se envía de una computadora en una red a otra computadora en
otra red ¿Pasa el paquete por el router?
Si, pasa por el router ya que primero el host A analiza si esta pertenece al host local, si no es así lo manda al router (la puerta de enlace predeterminada), el router busca en las tablas de enrutamiento (rutas estáticas, dinámicas o directamente conectadas) para ver donde esta el siguiente salto que conecta con la red solicitada, le avisa al host a que puede mandar los paquetes porque tiene la conmutación para poder enviar estos paquetes. 
* **¿Qué información indica a la computadora origen si la IP destino está en la**
**misma red (y puede enviarle paquetes directamente) o en una red diferente (y**
**debe enviar el paquete al router)?** 
La información que indica esto, es una operación que hace el SO : 
* Primero toma la dirección ip del host a, hace una operación AND bit a bit con la mascara de subred , y el resultado de esto es la dirección de red que pertenece el host A
* Después hace lo mismo con la IP del destinatario, para determinar si se encuentra en la misma red, si esta ip no pertenece a la misma red, entonces recurre al router, acá se utiliza el proceso ARP para obtener la MAC del router y para que el mismo encargue de llevar los datos al destinatario correspondiente
*200.21.120.66 AND 255.255.255.252 =200.21.120.64 
200.21.120.68 AND 255.255.255.252 = 200.21.120.68 (SON DISTINTAS REDES)
![[Pasted image 20251022143704.png]]

## ***ACTIVIDAD 4.3 SERVIDOR DHCP*** 
* *¿Cuales son las direcciones IP y MAC origen y destino del paquete DHCP request?.**
![[Pasted image 20251022171746.png]]
Como podemos apreciar en la anterior imagen, cuando el host hace un DHCP REQUEST para poder entablar una conexión con el servidor y que este le asigne una IP de forma dinámica, en el paquete formado por la cabecera de la ip, tenemos que el : 
* SRC IP: 0.0.0.0 
* DEST IP: 255.255.255.255 Esto asegura que todos en la red local procesen el paquete que esta enviando este host 
## ***Actividad 4.4 Paquetes desde una computadora NAT***
* **Al pasar un paquete por un servidor NAT: ¿Cambia la dirección Ethernet?, ¿Cambia la dirección IP?**
![[Pasted image 20251022172447.png]]
![[Pasted image 20251022172641.png]]
Al analizar los paquetes tanto que salieron de la PC12, como los que salen después del router, notamos que las ip ha sido transformada a la ip publica de la red NAT, esto lo hace gracias a la tabla NAT que nos ayuda a traducir las ip privada en publicas, y guardando el destino así cuando el receptor envíe el mensaje de nuevo hacia la red NAT el dispositivo utiliza la traducción necesaria para hacer llegar los datos a quien los solicito 