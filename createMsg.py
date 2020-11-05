import math
import serial
import serial.tools.list_ports


STX_START = 0x02
SUB_ADDRESS = 0x3030
SER_ID = 0x30
ETX_END = 0x03

def block_check_character(NODE, MRC, SRC, PAR, ADD, ELEM):

    bcc = (NODE>>8)^(NODE&0xFF)^(SUB_ADDRESS>>8)^(SUB_ADDRESS&0xFF)^SER_ID^MRC^SRC^(PAR>>8)^(PAR&0XFF)^(ADD>>8)^(ADD&0xFF)^(ELEM>>8)^(ELEM&0xFF)^ ETX_END
    return bcc
    
def hexar2str(hexar):
    return ''.join([chr(c) for c in hexar])
    
    
def create_msg(nodeNo, mrc, src, par, add, elem):

    bcc = block_check_character(nodeNo, mrc, src, par, add, elem)     

    msg = []
    msg.append(STX_START)
    msg.append(nodeNo)
    msg.append(SUB_ADDRESS)
    msg.append(SER_ID)
    msg.append(mrc)
    msg.append(src)
    msg.append(par)
    msg.append(add)
    msg.append(elem)
    msg.append(ETX_END)
    msg.append(bcc)
   
    print ("Message: %s" % (''.join([hex(b)+" " for b in msg])))
    msgStr = hexar2str(msg)
    return msgStr



comPorts = serial.tools.list_ports.comports()
print([port.device + ": " + port.hwid for port in comPorts])

nodeNo = 0x0001 
mrc = 0x02
src = 0x01
par = 0xC020
add = 0x3001
elem = 0x8001

msg = create_msg(nodeNo, mrc, src, par, add, elem)
print(msg)
print(msg.encode())

input("Ready")
ser = serial.Serial('COM5', 115200, timeout=1)  
# #ser.open()
ser.flushInput()
ser.flushOutput()
ser.write(msg.encode())    
# #ser.close() 

print("espera")
while True:
    response = ser.readline()
    print (response)



