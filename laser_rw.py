import re
import serial
import serial.tools.list_ports

class laser_options():
    def __init__(self, port):
        self.ser = serial.Serial(port, 115200, timeout=0.1)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.flush()        
        
        
    def wr_port(self, inst):
        msg = ''.join([chr(c) for c in inst])
        
        self.ser.write(msg.encode())
        response = self.ser.readline()

        return response
        
        
    def read_value(self):
        read_inst = [2, 48, 48, 48, 48, 48, 48, 50, 48, 49, 67, 48, 50, 48, 51, 48, 48, 48, 56, 48, 48, 49, 3, 75]
        response = self.wr_port(read_inst)
        
        
        if response[5] == 48 and response[6] == 48 and response[11] == 48 and response[12] == 48 and response[13] == 48 and response[14] == 48:
            print("Successful communication")
            
            if response[27] == 55 and response[28] == 70 and response[29] == 70 and response[30] == 70 and response[31] == 70 and response[32] == 70 and response[33] == 70 and response[34] == 70:
                print("Error during the measure")
                data_mm = "null"
                
            else: 
                response = response.decode()
                data = "0x" + response[27] + response[28] + response[29] + response[30] + response[31] + response[32] + response[33] + response[34]
                data = int(data, 16)
  
                if response[27] == "F":
                    data = (data -(1<<32))
                
                data_mm = float(data/1000000)
            
        else:
            print("Error during the communication")
            data_mm = "null"
            
        return data_mm
        
        
    def set_zero(self):
        zero_inst = [2, 48, 48, 48, 48, 48, 48, 50, 48, 50, 67, 48, 67, 51, 70, 48, 48, 48, 56, 48, 48, 49, 48, 48, 48, 48, 48, 48, 48, 49, 3, 78]
        response = self.wr_port(zero_inst)
         
        if response[5] == 48 and response[6] == 48:
            measure=laser.read_value()
            if (measure < 1) and (measure > -1): 
                result = "Successful"
            else:
                result = "Fail"
            
        else:
            result = "Fail"
    
        return result
        
 
def main():
    comPorts = serial.tools.list_ports.comports()
    laserCOM = "null"    
    
    for port in comPorts:
        if re.search('VID:PID=0590:004D', str(port.hwid)):
            laserCOM = port.device
            
    if laserCOM == "null":
        print("Laser not found")
        print("Connect it and start again")
        exit()
    
    print("Laser found at port: " + laserCOM)    
    laser = laser_options(laserCOM)
    
    while True:
        print("\n**************************************************************")
        opt = input("Do you want to: Read laser(R), Set Zero(Z) or Exit(E):  ")
        
        if opt == "R" or opt == "r":
            measure=laser.read_value()
            if measure == "null" :
                print("Please run again")
            else:
                print("The actual mesaure is: " + str(measure))
                
        elif opt == "Z" or opt == "z":
            status=laser.set_zero()
            print("Set Zero: " + status)
            
        elif opt == "E" or opt == "e":
            print("Exit")
            exit()
            
        else:
            print("Invalid option")
 
if __name__ == '__main__':
    main()
