import math
import serial
import serial.tools.list_ports


STX_START = 0x02
SUB_ADDRESS = 0x3030
SER_ID = 0x30
ETX_END = 0x03

def block_check_character(NODE, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24):

    #bcc = (NODE>>8)^(NODE&0xFF)^(SUB_ADDRESS>>8)^(SUB_ADDRESS&0xFF)^SER_ID^MRC^SRC^(PAR>>8)^(PAR&0XFF)^(ADD>>8)^(ADD&0xFF)^(ELEM>>8)^(ELEM&0xFF)^ ETX_END
    bcc = (NODE>>8)^(NODE&0xFF)^(SUB_ADDRESS>>8)^(SUB_ADDRESS&0xFF) ^ SER_ID^ m1 ^ m2 ^ m3 ^ m4 ^ m5 ^ m6 ^ m7 ^ m8 ^ m9 ^ m10 ^ m11 ^ m12 ^ m13 ^ m14 ^ m15 ^ m16 ^ m17 ^ m18 ^ m19 ^ m20 ^ m21 ^ m22 ^ m23 ^ m24 ^ ETX_END
    return bcc
    
def hexar2str(hexar):
    return ''.join([chr(c) for c in hexar])
    
    
def create_msg(nodeNo, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24):

    bcc = block_check_character(nodeNo, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24)   

    msg = []
    msg.append(STX_START)
    msg.append(nodeNo)
    msg.append(SUB_ADDRESS)
    msg.append(SER_ID)
    msg.append(m1)
    msg.append(m2)
    msg.append(m3) 
    msg.append(m4)
    msg.append(m5)
    msg.append(m6)
    msg.append(m7) 
    msg.append(m8)
    msg.append(m9)
    msg.append(m10)
    msg.append(m11) 
    msg.append(m12)
    msg.append(m13)
    msg.append(m14)
    msg.append(m15) 
    msg.append(m16)
    msg.append(m17)
    msg.append(m18)
    msg.append(m19) 
    msg.append(m20)
    msg.append(m21)
    msg.append(m22)
    msg.append(m23) 
    msg.append(m24)    
    msg.append(ETX_END)
    msg.append(bcc)
   
    print ("Message: %s" % (''.join([hex(b)+" " for b in msg])))
    msgStr = hexar2str(msg)
    return msgStr



comPorts = serial.tools.list_ports.comports()
print([port.device + ": " + port.hwid for port in comPorts])

nodeNo = 0x3030 
m1 = 0x30
m2 = 0x32
m3 = 0x30
m4 = 0x32
m5 = 0x43
m6 = 0x30
m7 = 0x30
m8 = 0x38
m9 = 0x46
m10 = 0x30
m11= 0x30
m12 = 0x30
m13 = 0x38
m14 = 0x30
m15 = 0x30
m16 = 0x31
m17 = 0x30
m18 = 0x30
m19 = 0x30
m20 = 0x30
m21 = 0x30
m22 = 0x30
m23 = 0x30
m24 = 0x30


msg = create_msg(nodeNo, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12, m13, m14, m15, m16, m17, m18, m19, m20, m21, m22, m23, m24)
print(msg)
print(msg.encode())

input("Ready")
ser = serial.Serial('COM4', 115200, timeout=2)  
# # #ser.open()
ser.flushInput()
ser.flushOutput()
ser.write(msg.encode())    
# # #ser.close() 

print("espera")
while True:
    response = ser.read()
    print (response)
