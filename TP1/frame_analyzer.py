
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

def is_ok_frame(frame):
    
    long = frame[2:6]
    long_dec = int(long, 16)
    long_frame = frame[6:-2]
    print(len(long_frame))
    if long_dec == len(long_frame) : 
        return True
    else : 
        return False

def counter_frame_ok(listf): 
    counter = 0
    for frame in listf : 
        if is_ok_frame(frame):
            counter += 1 
    return counter



with open('Tramas_802-15-4.log', 'r') as frame_log : 
    frame = frame_log.read() 


list_anal = framer_analyzer(frame)

print(len(list_anal))
print(counter_frame_ok(list_anal))