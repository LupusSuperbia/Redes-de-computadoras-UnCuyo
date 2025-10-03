## Corta las tramas por su bandera '7E' 
def framer_analyzer(frame) : 
    frame_list = []
    
    index = 0 
    while index != -1  :
        start = frame.find("7E", index)

        if start == -1 : 
            break 

        end = frame.find("7E", start + 1)

        while end != -1 and frame[end - 2: end] == "7D":
            end = frame.find("7E", end + 1)
        
        subframe = ''
        if end == -1 : 
            subframe = frame[start:]
            index = end
        elif end != -1: 
            subframe = frame[start:end]
            index = end
        frame_list.append(subframe)
    return frame_list

## Analiza si la longitud del frame es correcta o no 
def is_ok_frame(frame):
    if frame.find("7D7E") != -1 : 
       frame = frame.replace("7D7E", "7E")
    long = frame[2:6]
    long_dec = int(long, 16)
    long_frame = frame[6: -2]
    checksum = frame[-2:]

    if long_dec == len(long_frame)/2 : 
        return True
    else : 
        return False
## Cuenta Las longitudes correctas y las que no, esta las agrega a otra lista nueva para poder ser utilizada mas adelante 
def counter_frame_ok(listf): 
    tramas_ok = []
    tramas_not_ok = []
    imprimir_con_decoracion("Salida de funcion que cuenta la longitud, en la salida muestra el indice y la trama que es incorrecta")
    for ind, frame in enumerate(listf) : 
        if is_ok_frame(frame):
            tramas_ok.append(frame)
        else : 
            print(ind, frame)
            tramas_not_ok.append(frame)
    return tramas_ok, tramas_not_ok
## Un utils
def imprimir_con_decoracion(mensaje):
    print("===========================================")
    print(mensaje)
    print("===========================================")
##Esto es para ver si tiene un salto de linea, una forma de verificar si hay algun detalle que se escapo cuando hice la division de las tramas 
def tiene_salto_de_linea(list_frame):
    counter = 0
    for frame in list_frame:
        if frame.find(" ") != -1 :
            print("upsi")
        find_replace(list_frame, frame, "\n", "")
        ## Parecido a otro 
        counter += 1
    return counter
## Utils 
def find_replace(list_frame, frame, stringBusc, cambiar, mostrar = False):
    if frame.find(stringBusc) != -1 : 
        framex = frame.replace(stringBusc, cambiar)
        ind = list_frame.index(frame) 
        if mostrar : 
            print(ind, frame)
        list_frame.pop(ind)
        list_frame.insert(ind, framex)

## Suma el frame para al retornarlo podamos compararlo con el checksum 
def sumfr(frame)  :
    suma = 0 
    for i in range(0, len(frame), 2): 
        hexSum = frame[i] + frame[i+1]
        suma += int(hexSum, 16)
    return suma
## Funcion que analiza los checksum 
def checksum_is_ok(list_frame): 
    counter = 0
    counter_isnotok = 0
    imprimir_con_decoracion("Salida de funcion que cuenta los checksum, la salida muestra los incorrectos : " )
    for i,fr in enumerate(list_frame):
        if fr.find("7D7E") != -1 : 
            fr = fr.replace("7D7E", "7E")  
        checksum_frame = fr[-2:]
        long_frame = fr[6: -2]
        sumCheck = sumfr(long_frame)
        difSum = 0xFF & sumCheck
        checkSumByte = 0xFF - difSum 
        if int(checksum_frame, 16) == int(checkSumByte): 
            counter += 1
        else : 
            print(i, fr)
            counter_isnotok +=1
    return counter, counter_isnotok
        
## Funcion que cuenta las tramas con secuencia de escape 
def con_sec_escape(list_frame): 
    counter = 0 
    imprimir_con_decoracion("Salida funcion que cuenta las tramas con Secuencia de Escape:")   
    for i,frm in enumerate(list_frame) : 
        if frm.find("7D7E") != -1 : 
            counter += 1
            print(i, frm)  
            frame = frm.replace("7D7E", "7E")
            list_frame.pop(i)
            list_frame.insert(i, frame) 
    return counter


if __name__ == "__main__":
    try:
        with open('Tramas_802-15-4.log', 'r') as frame_log : 
            frame = frame_log.read()
            
        list_anal = framer_analyzer(frame)
        tiene_salto_de_linea(list_anal)
        
        tramasOk, tramasnotOk = counter_frame_ok(list_anal)
        checkSumOk, checkSumNotOK = checksum_is_ok(tramasOk)
        sec_escape = con_sec_escape(tramasOk)
        print("Tramas Totales:", len(list_anal))
        print("Tramas con longitud correcta:", len(tramasOk), "\nTramas con longitud incorrecta:", len(tramasnotOk))
        print("CheckSum que son correctos :", checkSumOk, "\nCheckSum que son incorrectos: ", checkSumNotOK) 
        print("Total de tramas con secuencia de escape : ", sec_escape )
 

    except FileNotFoundError:
        print("Error: El archivo 'Tramas_802-15-4.log' no se encuentra.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

