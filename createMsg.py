import math
import serial
import serial.tools.list_ports


STX_START = 0x02
SUB_ADDRESS = 0x3030
SER_ID = 0x30
ETX_END = 0x03

def block_check_character(NODE, MRC, SRC, VAR, ADD, BIT, ELEM):

    bcc = (NODE>>8)^(NODE&0xFF)^(SUB_ADDRESS>>8)^(SUB_ADDRESS&0xFF)^SER_ID^MRC^SRC^VAR^(ADD>>8)^(ADD&0xFF)^BIT^(ELEM>>8)^(ELEM&0xFF)^ ETX_END
    return bcc
    
def hexar2str(hexar):
    return ''.join([chr(c) for c in hexar])
    
    
def create_msg(nodeNo, mrc, src, var, add, bit, elem):

    bcc = block_check_character(nodeNo, mrc, src, var, add, bit, elem)     
 
    msg = []
    msg.append(STX_START)
    msg.append(nodeNo)
    msg.append(SUB_ADDRESS)
    msg.append(SER_ID)
    msg.append(mrc)
    msg.append(src)
    msg.append(var)
    msg.append(add)
    msg.append(bit)
    msg.append(elem)
    msg.append(ETX_END)
    msg.append(bcc)
   
    print ("Message: %s" % (''.join([hex(b)+" " for b in msg])))
    msgStr = hexar2str(msg)
    return msgStr



comPorts = serial.tools.list_ports.comports()
print([port.device + ": " + port.hwid for port in comPorts])

nodeNo = 0x3030 
mrc = 0x33
src = 0x30
var = 0x30
add = 0x3533
bit = 0x30
elem = 0x3031

msg = create_msg(nodeNo, mrc, src, var, add, bit, elem)
print(msg)





