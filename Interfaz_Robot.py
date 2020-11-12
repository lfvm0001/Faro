from laser_rw import laser_options
import serial.tools.list_ports
from tkinter import ttk
from tkinter import *
import serial
import time
import re
import os

    
class GUI():
    def __init__(self, window):
        self.file = time.strftime("%Y%m%d-%H%M%S") + ".txt"
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
                pose = "0,"+self.x_txt.get()+","+self.y_txt.get()+","+self.z_txt.get()+","+self.rx_txt.get()+","+self.ry_txt.get()+","+self.rz_txt.get()+";\n"
                
                try:
                    self.msj_text.insert(INSERT, "Enviando posición al robot...\n")
                    self.msj_text.see(END)
                    robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
                    robotS.flushInput()
                    robotS.flushOutput()
                    robotS.flush() 
                    robotS.write(str(pose).encode('utf-8'))
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
        
            pose = "3,0,0,0,0,0,0;\n"
            
            try:
                self.msj_text.insert(INSERT, "Leyendo posición al robot...\n")
                self.msj_text.see(END)
                robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
                robotS.flushInput()
                robotS.flushOutput()
                robotS.flush() 
                robotS.write(str(pose).encode('utf-8'))
                response = robotS.read_until('\n',None)
                response = response.decode()
                response = response.rstrip()
                
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
        self.robotMeasure.set("")
        self.laserMeasure.set("")
        
        self.readRobotCB()
        self.readLaserCB()

        tableRobot = "table" + str(self.punto) + "0"
        tableLaser = "table" + str(self.punto) + "1"
        
        exec("self." + tableRobot + ".delete(0,END)")
        exec("self." + tableRobot + ".insert(0,'" + self.robotMeasure.get() + "')")
        exec("self." + tableLaser + ".delete(0,END)")
        exec("self." + tableLaser + ".insert(0,'" + self.laserMeasure.get() + "')")
        
        file = open(self.file,"a") 
        file.write("'" + self.robotMeasure.get() + "' ") 
        file.write("'" + self.laserMeasure.get() + "'\n") 
        file.close()
        self.msj_text.insert(INSERT, "Punto guardado en " + self.file +" ...\n")
        self.msj_text.see(END)
        
        if self.punto == 5:
            self.punto = 0
        else:
            self.punto = self.punto + 1


    def consulta(pos_enviada):
        fin = 0
        
        robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
        robotS.flushInput()
        robotS.flushOutput()
        robotS.flush() 
        
        cmd = "3,0,0,0,0,0,0;\n"
        
        while(fin==0):
        
            robotS.write(str(cmd).encode('utf-8'))
            pos_actual = robotS.read_until('\n',None)
                        
            pos_actual = pos_actual.decode()
            pos_actual = pos_actual.split(" ")

            pos_actual_int = [0,0,0,0,0,0]
            ind = 0
            
            for i in pos_actual:
                if not (i==""):
                    pos_actual_int[ind] = float(i)
                    
                    if(ind==5):
                        break
                    ind = ind+1
                    
            if pos_actual_int[0]==pos_enviada[0] and pos_actual_int[1]==pos_enviada[1] and pos_actual_int[2]==pos_enviada[2] and pos_actual_int[3]==pos_enviada[3] and pos_actual_int[4]==pos_enviada[4] and pos_actual_int[5]==pos_enviada[5]:
                fin = 1


    def startAutoCB(self):
        self.autoMsj_text.insert(INSERT, "Verificando puertos...\n")
        self.autoMsj_text.see(END)
        
        self.actualizarCB()
        
        if self.robotPort.get() == "Sin conexión" or self.laserPort.get() == "Sin conexión":
            self.autoMsj_text.insert(INSERT, "Para comenzar, conectar el robot y el laser ..\n")
            self.autoMsj_text.see(END)
        else:
            if os.path.exists(self.file):
                os.remove(self.file)
            
            x=[[0,0,0,0,0,0],
            [57.46,47.6,100.56,0.01,-59.03,0],#refA
            [-8.93,47.59,100.56,0.01,-59.03,0],
            [35.57,103.44,-5.59,0.01,-7.05,0],#refB
            [-5.54,103.43,-5.59,0.01,-7.05,0],
            [35.7,107.89,-10.22,0.06,-7.38,0],#refC
            [6.26,107.89,-10.22,0.06,-7.38,0],
            [45.3,61.69,75.78,0.06,-47.08,0],#refD
            [6.45,61.69,75.78,0.06,-47.08,0],
            [47.81,26.33,132.83,0.06,-70.11,0],#refE,
            [1.73,26.33,132.83,0.06,-70.11,0],
            [0,0,0,0,0,0]];
            
            for  i in range(0, len(x)):
                x1 = "0,"+str(x[i][0])+","+str(x[i][1])+","+ str(x[i][2])+","+str(x[i][3])+","+str(x[i][4])+","+str(x[i][5])+";\n"
                robotS = serial.Serial(self.robotPort.get(), 115200, timeout=1)
                robotS.flushInput()
                robotS.flushOutput()
                robotS.flush() 
                robot.write(str(x1).encode('utf-8'))

                self.autoMsj_text.insert(INSERT, "Posición " + str(i+1) + " enviada: " + x[i] + "...\n")
                self.autoMsj_text.see(END)

                self.consulta(x[i])
                
                if i==1 or i==3 or i==5 or i==7 or i==9:
                    self.setZeroCB()
                if i==2 or i==4 or i==6 or i==8 or i==10:
                    self.readRobotCB()
                    self.readLaserCB()
                    
                    self.autoMsj_text.insert(INSERT, "Lectura de laser: " + self.laserMeasure.get() + "...\n")
                    self.autoMsj_text.see(END)
                    
                    file = open(self.file,"a") 
                    file.write("'" + self.robotMeasure.get() + "' ") 
                    file.write("'" + self.laserMeasure.get() + "'\n") 
                    file.close()
                    
            self.autoMsj_text.insert(INSERT, "Puntos guardados en " + self.file +" ...\n")
            self.autoMsj_text.see(END)
  
  
    #Create GUI
    def create(self):
        self.window.title("Interfaz Robot")
        
        self.window_height = 560
        self.window_width  = 720
        
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.window_width/2))
        y_cordinate = int((screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, x_cordinate, y_cordinate))
        
        tabControl = ttk.Notebook(self.window)
        tabManual = Frame(tabControl)
        tabAuto = Frame(tabControl)
        
        tabControl.add(tabManual, text='Manual') 
        tabControl.add(tabAuto, text='Auto') 
        tabControl.pack(expand = 1, fill ="both")
        
        port_frame = LabelFrame(tabManual, text="Puertos")
        port_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        pose_frame = LabelFrame(tabManual, text="Mover robot")
        pose_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        cmds_frame = LabelFrame(tabManual, text="Comandos")
        cmds_frame.grid(row=0, column=1, sticky="nsew", padx=5,pady=10)
        data_frame = LabelFrame(tabManual, text="Puntos")
        data_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=10)
        info_frame = LabelFrame(tabManual, text="Información")
        info_frame.grid(row=2, column=0, sticky="nsew", padx=15, pady=5, columnspan=2)
        
        portAuto_frame = LabelFrame(tabAuto, text="Secuencia Automática")
        portAuto_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        infoAuto_frame = LabelFrame(tabAuto, text="Estado")
        infoAuto_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        startAuto_buttom = Button(tabAuto, text='Empezar', command=self.startAutoCB, width=20)
        startAuto_buttom.grid(row=2, column=0, padx=10, pady=10)
        
        
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
        clear_buttom = Button(pose_frame, text=' Limpiar ', command=self.clearCB, width=5)
        clear_buttom.grid(row=2, column=5, padx=10, pady=10)

        #Componentes de cmds_frame
        readLaser_buttom = Button(cmds_frame, text='Obtener medida laser:', command=self.readLaserCB, width=20)
        readLaser_buttom.grid(row=0, column=0, padx=10, pady=10)
        medida_laser = Message(cmds_frame, textvariable=self.laserMeasure, bg="white", justify=LEFT, width=1000)
        medida_laser.grid(row=0, column=1, padx=5)
        
        readRobot_buttom = Button(cmds_frame, text='Obtener posición robot:', command=self.readRobotCB, width=20)
        readRobot_buttom.grid(row=1, column=0, padx=10, pady=10)
        medida_robot = Message(cmds_frame, textvariable=self.robotMeasure, bg="white", justify=LEFT, width=1000)
        medida_robot.grid(row=1, column=1, padx=5)
        
        self.laserMeasure.set("                                             ")
        self.robotMeasure.set("                                             ")
        
        setZero_buttom = Button(cmds_frame, text='Reiniciar referencia', command=self.setZeroCB, width=20)
        setZero_buttom.grid(row=2, column=0, padx=10, pady=10)
        savePoint_buttom = Button(cmds_frame, text='Guadar Punto', command=self.savePointCB, width=20)
        savePoint_buttom.grid(row=2, column=1, padx=10, pady=10)
        
        #Componentes de data_frame
        self.table00 = Entry(data_frame, width=25, justify='center')
        self.table10 = Entry(data_frame, width=25, justify='center')        
        self.table20 = Entry(data_frame, width=25, justify='center')       
        self.table30 = Entry(data_frame, width=25, justify='center')
        self.table40 = Entry(data_frame, width=25, justify='center')
        self.table50 = Entry(data_frame, width=25, justify='center')
        self.table01 = Entry(data_frame, width=25, justify='center')
        self.table11 = Entry(data_frame, width=25, justify='center')
        self.table21 = Entry(data_frame, width=25, justify='center')
        self.table31 = Entry(data_frame, width=25, justify='center')
        self.table41 = Entry(data_frame, width=25, justify='center')
        self.table51 = Entry(data_frame, width=25, justify='center')
        
        self.table00.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')
        self.table10.grid(row=1, column=0, padx=10, pady=5, sticky='nsew')
        self.table20.grid(row=2, column=0, padx=10, pady=5, sticky='nsew')
        self.table30.grid(row=3, column=0, padx=10, pady=5, sticky='nsew')
        self.table40.grid(row=4, column=0, padx=10, pady=5, sticky='nsew')
        self.table50.grid(row=5, column=0, padx=10, pady=5, sticky='nsew')
        self.table01.grid(row=0, column=1, padx=10, pady=5, sticky='nsew')
        self.table11.grid(row=1, column=1, padx=10, pady=5, sticky='nsew')
        self.table21.grid(row=2, column=1, padx=10, pady=5, sticky='nsew')
        self.table31.grid(row=3, column=1, padx=10, pady=5, sticky='nsew')
        self.table41.grid(row=4, column=1, padx=10, pady=5, sticky='nsew')
        self.table51.grid(row=5, column=1, padx=10, pady=5, sticky='nsew')
        
        #Componentes de info_frame
        self.msj_text = Text(info_frame, height=5, width=80)
        self.msj_text.insert(INSERT, "Esperando comandos...\n")
        self.msj_text.see(END)
        self.msj_text.grid(row=0, column=0, padx=10, pady=10)
        
        scroll = Scrollbar(info_frame, command=self.msj_text.yview)
        scroll.grid(row=0, column=2, sticky='nsew')
        self.msj_text['yscrollcommand'] = scroll.set
        
        #Componentes de portAuto_frame
        laserAuto_lbl = Label(portAuto_frame, text="Laser:")
        laserAuto_lbl.grid(row=0, column=0, padx=10, pady=10)
        robotAuto_lbl = Label(portAuto_frame, text="Robot:")
        robotAuto_lbl.grid(row=1, column=0, padx=10, pady=10)
        laserAuto_port = Message(portAuto_frame, textvariable=self.laserPort, bg="white", justify=LEFT, width=200)
        laserAuto_port.grid(row=0, column=1)
        robotAuto_port = Message(portAuto_frame, textvariable=self.robotPort, bg="white", justify=LEFT, width=200)
        robotAuto_port.grid(row=1, column=1)
        
        #Componentes de infoAuto_frame
        self.autoMsj_text = Text(infoAuto_frame, height=17, width=80)
        self.autoMsj_text.insert(INSERT, "Esperando..\n")
        self.autoMsj_text.see(END)
        self.autoMsj_text.grid(row=0, column=0, padx=10, pady=10)
        
        scroll = Scrollbar(infoAuto_frame, command=self.autoMsj_text.yview)
        scroll.grid(row=0, column=2, sticky='nsew')
        self.autoMsj_text['yscrollcommand'] = scroll.set
        
         
def main():

    window = Tk()
    gui = GUI(window)
    gui.create()
    gui.actualizarCB()
    window.mainloop()


if __name__ == '__main__':
    main()
