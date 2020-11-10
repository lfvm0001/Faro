from tkinter import *
import serial

def actualizarCB():
    print("Actualizar")
    
def enviarCB():
    print("Enviar")
    
def clearCB():
    print("Clear")
    
def readLaserCB():
    print("Read Laser")
    
def readRobotCB():
    print("Read Robot")

def setZeroCB():
    print("Set zero")
    
def savePointCB():
    print("Save point")
    
    
def create_GUI(window):
    
    window.title("Interfaz Robot")
    
    window_height = 500
    window_width  = 690
    
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))

    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    port_frame = LabelFrame(window, text="Puertos")
    port_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    pose_frame = LabelFrame(window, text="Mover robot")
    pose_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    cmds_frame = LabelFrame(window, text="Comandos")
    cmds_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
    data_frame = LabelFrame(window, text="Puntos")
    data_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
    info_frame = LabelFrame(window, text="Información")
    info_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10, columnspan=2)
    
    
    #Componentes de port_frame
    laserPort = StringVar()
    robotPort = StringVar()
    
    laser_lbl = Label(port_frame, text="Laser:")
    laser_lbl.grid(row=0, column=0, padx=10, pady=10)
    robot_lbl = Label(port_frame, text="Robot:")
    robot_lbl.grid(row=1, column=0, padx=10, pady=10)
    laser_port = Message(port_frame, textvariable=laserPort, bg="white", justify=LEFT, width=100)
    laser_port.grid(row=0, column=1)
    robot_port = Message(port_frame, textvariable=robotPort, bg="white", justify=LEFT, width=100)
    robot_port.grid(row=1, column=1)
    act_buttom = Button(port_frame, text ="Actualizar", command = actualizarCB, width=10)
    act_buttom.grid(row=2, column=1, padx=10, pady=10)
  
    laserPort.set("Sin conexión")
    robotPort.set("Sin conexión")
    
    #Componentes de pose_frame
    x_lbl = Label(pose_frame, text='x')
    x_lbl.grid(row=0, column=0, padx=10, pady=10)
    x_txt = Entry(pose_frame, width=7)
    x_txt.grid(row=0, column=1, padx=10, pady=10)
    y_lbl = Label(pose_frame, text='y')
    y_lbl.grid(row=0, column=2, padx=10, pady=10)
    y_txt = Entry(pose_frame, width=7)
    y_txt.grid(row=0, column=3, padx=10, pady=10)
    z_lbl = Label(pose_frame, text='z')
    z_lbl.grid(row=0, column=4, padx=10, pady=10)
    z_txt = Entry(pose_frame, width=7)
    z_txt.grid(row=0, column=5, padx=10, pady=10)
    
    rx_lbl = Label(pose_frame, text='rx')
    rx_lbl.grid(row=1, column=0, padx=10, pady=10)
    rx_txt_rx=Entry(pose_frame, width=7)
    rx_txt_rx.grid(row=1, column=1, padx=10, pady=10)
    ry_lbl = Label(pose_frame, text='ry')
    ry_lbl.grid(row=1, column=2, padx=10, pady=10)
    ry_txt_ry = Entry(pose_frame, width=7)
    ry_txt_ry.grid(row=1, column=3, padx=10, pady=10)
    rz_lbl = Label(pose_frame, text='rz')
    rz_lbl.grid(row=1, column=4, padx=10, pady=10)
    rz_txt = Entry(pose_frame, width=7)
    rz_txt.grid(row=1, column=5, padx=10, pady=10)
    
    env_buttom = Button(pose_frame, text='Enviar', command=enviarCB, width=5)
    env_buttom.grid(row=2, column=3, padx=10, pady=10)
    clear_buttom = Button(pose_frame, text='Clear', command=clearCB, width=5)
    clear_buttom.grid(row=2, column=5, padx=10, pady=10)

    #Componentes de port_frame
    laserMeasure = StringVar()
    robotMeasure = StringVar()
    
    readLaser_buttom = Button(cmds_frame, text='Obtener medida laser:', command=readLaserCB, width=20)
    readLaser_buttom.grid(row=0, column=0, padx=10, pady=10)
    medida_laser = Message(cmds_frame, textvariable=laserMeasure, bg="white", justify=LEFT, width=1000)
    medida_laser.grid(row=0, column=1)
    
    readRobot_buttom = Button(cmds_frame, text='Obtener posición robot:', command=readRobotCB, width=20)
    readRobot_buttom.grid(row=1, column=0, padx=10, pady=10)
    medida_robot = Message(cmds_frame, textvariable=robotMeasure, bg="white", justify=LEFT, width=1000)
    medida_robot.grid(row=1, column=1)
    
    laserMeasure.set("                                             ")
    robotMeasure.set("                                             ")
    
    setZero_buttom = Button(cmds_frame, text='Reiniciar referencia', command=setZeroCB, width=20)
    setZero_buttom.grid(row=2, column=0, padx=10, pady=10)
    savePoint_buttom = Button(cmds_frame, text='Guadar Punto', command=savePointCB, width=20)
    savePoint_buttom.grid(row=2, column=1, padx=10, pady=10)
    
    #Componentes de data_frame
    
    #Componentes de info_frame
    msj_text = Text(info_frame, height=5, width=80)
    msj_text.insert(INSERT, "Ready to use.....")
    msj_text.grid(row=0, column=0, padx=10, pady=10)
    
  

if __name__ == '__main__':
    
    window=Tk()
    create_GUI(window)
    window.mainloop()
