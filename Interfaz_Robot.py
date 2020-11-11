import serial.tools.list_ports
from laser_rw import laser_options
from tkinter import *
import serial
import re

    
class GUI():
    def __init__(self, window):
        self.window = window
        self.laserPort = StringVar()
        self.robotPort = StringVar()
        self.laserMeasure = StringVar()
        self.robotMeasure = StringVar()
        self.punto = 0


    #Funciones
    def actualizarCB(self):
        laser = False
        robot = False
        comPorts = serial.tools.list_ports.comports()

        for port in comPorts:
            if re.search('VID:PID=0590:004D', str(port.hwid)):
                self.laserPort.set(str(port.device))
                laser = True
                self.msj_text.insert(INSERT, "Laser: " + str(port.device) + "\n")
                self.msj_text.see(END)

            if re.search('VID:PID=067B:2303', str(port.hwid)):
                self.robotPort.set(str(port.device))
                robot = True
                self.msj_text.insert(INSERT, "Robot: " + str(port.device) + "\n")
                self.msj_text.see(END)

        if laser == False:
            self.laserPort.set("Sin conexión")
            self.msj_text.insert(INSERT, "Robot no encontrado en ningún puerto...En caso de conexion, actualizar puertos \n")
            self.msj_text.see(END)
            
        if robot == False:
            self.robotPort.set("Sin conexión")
            self.msj_text.insert(INSERT, "Laser no encontrado en ningún puerto...En caso de conexion, actualizar puertos \n")
            self.msj_text.see(END)
            
            
    def enviarCB(self):
        self.actualizarCB()
        if self.robotPort.get() == "Sin conexión":
            self.msj_text.insert(INSERT, "Para enviar posición, verificar conexión del robot ..\n")
            self.msj_text.see(END)
        else:
        
            if self.x_txt.get() == "" or self.y_txt.get() == "" or self.z_txt.get() == "" or self.rx_txt.get() == "" or self.ry_txt.get() == "" or self.rz_txt.get() == "":
                self.msj_text.insert(INSERT, "No debe dejar ninguna coordenada sin asignar..\n")
                self.msj_text.see(END)
            else:
                pose = "0;"+self.x_txt.get()+";"+self.y_txt.get()+";"+self.z_txt.get()+";"+self.rx_txt.get()+";"+self.ry_txt.get()+";"+self.rz_txt.get()+";\n"
                
                try:
                    self.msj_text.insert(INSERT, "Enviando posición al robot...\n")
                    self.msj_text.see(END)
                    robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
                    robotS.flushInput()
                    robotS.flushOutput()
                    robotS.flush() 
                    robotS.write(str(pose).encode('utf-8'))
                    response=robotS.read_until('\n',None)
                    self.msj_text.insert(INSERT, "Posición enviada correctamente...\n")
                    self.msj_text.see(END)
                
                except:
                    self.msj_text.insert(INSERT, "Error en la conexión con Robot...Reintentar...\n")
                    self.msj_text.see(END)
        
        
    def clearCB(self):
        self.x_txt.delete(0,END)
        self.x_txt.insert(0,"0")
        self.y_txt.delete(0,END)
        self.y_txt.insert(0,"0")
        self.z_txt.delete(0,END)
        self.z_txt.insert(0,"0")
        self.rx_txt.delete(0,END)
        self.rx_txt.insert(0,"0")
        self.ry_txt.delete(0,END)
        self.ry_txt.insert(0,"0")
        self.rz_txt.delete(0,END)
        self.rz_txt.insert(0,"0")
        
        self.msj_text.insert(INSERT, "Contenido de casillas eliminado...\n")
        self.msj_text.see(END)
        
        
    def readLaserCB(self):
        self.actualizarCB()
        if self.laserPort.get() == "Sin conexión":
            self.msj_text.insert(INSERT, "Para realizar lectura, verificar conexión del laser ..\n")
            self.msj_text.see(END)
        else:
            self.msj_text.insert(INSERT, "Realizando medición de laser...\n")
            self.msj_text.see(END)
            laser = laser_options(self.laserPort.get())
            measure = laser.read_value()
        
            if measure == "null" :
                self.msj_text.insert(INSERT, "Error durante la medición...Reintentar...\n")
                self.msj_text.see(END)
            else:
                self.laserMeasure.set(measure)
                self.msj_text.insert(INSERT, "Medición de laser finalizó correctamente...\n")
                self.msj_text.see(END)
        
        
    def readRobotCB(self):
        self.actualizarCB()
        if self.robotPort.get() == "Sin conexión":
            self.msj_text.insert(INSERT, "Para leer posición, verificar conexión del robot ..\n")
            self.msj_text.see(END)
        else:
        
            pose = "3;"+self.x_txt.get()+";"+self.y_txt.get()+";"+self.z_txt.get()+";"+self.rx_txt.get()+";"+self.ry_txt.get()+";"+self.rz_txt.get()+";\n"
            
            try:
                self.msj_text.insert(INSERT, "Leyendo posición al robot...\n")
                self.msj_text.see(END)
                robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
                robotS.flushInput()
                robotS.flushOutput()
                robotS.flush() 
                robotS.write(str(pose).encode('utf-8'))
                response=robotS.read_until('\n',None)
                
                self.robotMeasure.set(response)
                self.msj_text.insert(INSERT, "Medición de posición finalizó correctamente...\n")
                self.msj_text.see(END)

            except:
                self.msj_text.insert(INSERT, "Error en la conexión con Robot...Reintentar...\n")
                self.msj_text.see(END)
            

    def setZeroCB(self):
        self.actualizarCB()
        if self.laserPort.get() == "Sin conexión":
            self.msj_text.insert(INSERT, "Para reiniciar la referencia, verificar conexión del laser ..\n")
            self.msj_text.see(END)
        else:
            self.msj_text.insert(INSERT, "Reiniciando la referencia del laser...\n")
            self.msj_text.see(END)
            laser = laser_options(self.laserPort.get())
            status = laser.set_zero()
            self.msj_text.insert(INSERT, "Reiniciar la referencia: " + status)
            self.msj_text.see(END)
        
        
    def savePointCB(self):
        if self.punto == 0:
            self.table00.delete(0,END)
            self.table00.insert(0,self.robotMeasure.get())
            self.table01.delete(0,END)
            self.table01.insert(0,self.laserMeasure.get())
            
            self.punto = 1
        
        elif self.punto == 1:
            self.table10.delete(0,END)
            self.table10.insert(0,self.robotMeasure.get())
            self.table11.delete(0,END)
            self.table11.insert(0,self.laserMeasure.get())
            
            self.punto = 2
            
        elif self.punto == 2:
            self.table20.delete(0,END)
            self.table20.insert(0,self.robotMeasure.get())
            self.table21.delete(0,END)
            self.table21.insert(0,self.laserMeasure.get())
            
            self.punto = 3
            
        elif self.punto == 3:
            self.table30.delete(0,END)
            self.table30.insert(0,self.robotMeasure.get())
            self.table31.delete(0,END)
            self.table31.insert(0,self.laserMeasure.get())
            
            self.punto = 4
        
        elif self.punto == 4:
            self.table40.delete(0,END)
            self.table40.insert(0,self.robotMeasure.get())
            self.table41.delete(0,END)
            self.table41.insert(0,self.laserMeasure.get())
            
            self.punto = 5
            
        else:
            self.table50.delete(0,END)
            self.table50.insert(0,self.robotMeasure.get())
            self.table51.delete(0,END)
            self.table51.insert(0,self.laserMeasure.get())
            
            self.punto = 0
        
        self.msj_text.insert(INSERT, "Punto guardado...\n")
        self.msj_text.see(END)
        
   
    #Create GUI
    def create(self):
        self.window.title("Interfaz Robot")
        
        self.window_height = 530
        self.window_width  = 705
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.window_width/2))
        y_cordinate = int((screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_cordinate, y_cordinate))
        
        port_frame = LabelFrame(self.window, text="Puertos")
        port_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        pose_frame = LabelFrame(self.window, text="Mover robot")
        pose_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        cmds_frame = LabelFrame(self.window, text="Comandos")
        cmds_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        data_frame = LabelFrame(self.window, text="Puntos")
        data_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        info_frame = LabelFrame(self.window, text="Información")
        info_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
        
        
        #Componentes de port_frame
        laser_lbl = Label(port_frame, text="Laser:")
        laser_lbl.grid(row=0, column=0, padx=10, pady=10)
        robot_lbl = Label(port_frame, text="Robot:")
        robot_lbl.grid(row=1, column=0, padx=10, pady=10)
        laser_port = Message(port_frame, textvariable=self.laserPort, bg="white", justify=LEFT, width=100)
        laser_port.grid(row=0, column=1)
        robot_port = Message(port_frame, textvariable=self.robotPort, bg="white", justify=LEFT, width=100)
        robot_port.grid(row=1, column=1)
        act_buttom = Button(port_frame, text ="Actualizar", command = self.actualizarCB, width=10)
        act_buttom.grid(row=2, column=1, padx=10, pady=10)
      
        self.laserPort.set("Sin conexión")
        self.robotPort.set("Sin conexión")
        
        #Componentes de pose_frame
        x_lbl = Label(pose_frame, text='x')
        x_lbl.grid(row=0, column=0, padx=10, pady=10)
        self.x_txt = Entry(pose_frame, width=7)
        self.x_txt.grid(row=0, column=1, padx=10, pady=10)
        y_lbl = Label(pose_frame, text='y')
        y_lbl.grid(row=0, column=2, padx=10, pady=10)
        self.y_txt = Entry(pose_frame, width=7)
        self.y_txt.grid(row=0, column=3, padx=10, pady=10)
        z_lbl = Label(pose_frame, text='z')
        z_lbl.grid(row=0, column=4, padx=10, pady=10)
        self.z_txt = Entry(pose_frame, width=7)
        self.z_txt.grid(row=0, column=5, padx=10, pady=10)
        
        rx_lbl = Label(pose_frame, text='rx')
        rx_lbl.grid(row=1, column=0, padx=10, pady=10)
        self.rx_txt = Entry(pose_frame, width=7)
        self.rx_txt.grid(row=1, column=1, padx=10, pady=10)
        ry_lbl = Label(pose_frame, text='ry')
        ry_lbl.grid(row=1, column=2, padx=10, pady=10)
        self.ry_txt = Entry(pose_frame, width=7)
        self.ry_txt.grid(row=1, column=3, padx=10, pady=10)
        rz_lbl = Label(pose_frame, text='rz')
        rz_lbl.grid(row=1, column=4, padx=10, pady=10)
        self.rz_txt = Entry(pose_frame, width=7)
        self.rz_txt.grid(row=1, column=5, padx=10, pady=10)
        
        env_buttom = Button(pose_frame, text='Enviar', command=self.enviarCB, width=5)
        env_buttom.grid(row=2, column=3, padx=10, pady=10)
        clear_buttom = Button(pose_frame, text='Limpiar', command=self.clearCB, width=5)
        clear_buttom.grid(row=2, column=5, padx=10, pady=10)

        #Componentes de cmds_frame
        readLaser_buttom = Button(cmds_frame, text='Obtener medida laser:', command=self.readLaserCB, width=20)
        readLaser_buttom.grid(row=0, column=0, padx=10, pady=10)
        medida_laser = Message(cmds_frame, textvariable=self.laserMeasure, bg="white", justify=LEFT, width=1000)
        medida_laser.grid(row=0, column=1)
        
        readRobot_buttom = Button(cmds_frame, text='Obtener posición robot:', command=self.readRobotCB, width=20)
        readRobot_buttom.grid(row=1, column=0, padx=10, pady=10)
        medida_robot = Message(cmds_frame, textvariable=self.robotMeasure, bg="white", justify=LEFT, width=1000)
        medida_robot.grid(row=1, column=1)
        
        self.laserMeasure.set("                                             ")
        self.robotMeasure.set("                                             ")
        
        setZero_buttom = Button(cmds_frame, text='Reiniciar referencia', command=self.setZeroCB, width=20)
        setZero_buttom.grid(row=2, column=0, padx=10, pady=10)
        savePoint_buttom = Button(cmds_frame, text='Guadar Punto', command=self.savePointCB, width=20)
        savePoint_buttom.grid(row=2, column=1, padx=10, pady=10)
        
        #Componentes de data_frame
        self.table00 = Entry(data_frame, width=25)
        self.table10 = Entry(data_frame, width=25)        
        self.table20 = Entry(data_frame, width=25)       
        self.table30 = Entry(data_frame, width=25)
        self.table40 = Entry(data_frame, width=25)
        self.table50 = Entry(data_frame, width=25)
        self.table01 = Entry(data_frame, width=25)
        self.table11 = Entry(data_frame, width=25)
        self.table21 = Entry(data_frame, width=25)
        self.table31 = Entry(data_frame, width=25)
        self.table41 = Entry(data_frame, width=25)
        self.table51 = Entry(data_frame, width=25)
        
        self.table00.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.table10.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.table20.grid(row=2, column=0, padx=5, pady=5, sticky='nsew')
        self.table30.grid(row=3, column=0, padx=5, pady=5, sticky='nsew')
        self.table40.grid(row=4, column=0, padx=5, pady=5, sticky='nsew')
        self.table50.grid(row=5, column=0, padx=5, pady=5, sticky='nsew')
        self.table01.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.table11.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')
        self.table21.grid(row=2, column=1, padx=5, pady=5, sticky='nsew')
        self.table31.grid(row=3, column=1, padx=5, pady=5, sticky='nsew')
        self.table41.grid(row=4, column=1, padx=5, pady=5, sticky='nsew')
        self.table51.grid(row=5, column=1, padx=5, pady=5, sticky='nsew')
        
        #Componentes de info_frame
        self.msj_text = Text(info_frame, height=5, width=80)
        self.msj_text.insert(INSERT, "Esperando comandos...\n")
        self.msj_text.see(END)
        self.msj_text.grid(row=0, column=0, padx=10, pady=10)
        
        scroll = Scrollbar(info_frame, command=self.msj_text.yview)
        scroll.grid(row=0, column=1, sticky='nsew')
        self.msj_text['yscrollcommand'] = scroll.set
        
        
def main():

    window=Tk()
    gui=GUI(window)
    gui.create()
    gui.actualizarCB()
    window.mainloop()


if __name__ == '__main__':
    main()
