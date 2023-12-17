import winreg
import win32com.client
import json
import os
import ctypes
import time
import platform
import datetime
import sys
import threading
from win11toast import toast
from tkinter import messagebox
import psutil
from plyer import notification
from PyQt5 import QtCore, uic,QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,QTableWidgetItem, QShortcut
from PyQt5.QtGui import QPalette, QColor,QBrush,QKeySequence

NewProcessPID = []
NewProcessName = []
NewProcessCmdLine = []
NewProcessMemUsage = []
NewProcessRunTime = []

NewAutoRunName = []
CurrentlyRunning = []
NewAutoRunPath = []
class MainUI(QMainWindow):
    def __init__(self):
        
        super(MainUI,self).__init__()
        self.setWindowTitle("MAIN CONTROL CENTER")
        uic.loadUi("UI.ui",self)
        self.Pages.setCurrentIndex(1)
        self.Discord.clicked.connect(self.OpenDiscord)

        self.ProcessViewT.setColumnWidth(3,800)
        self.ProcessViewT.setColumnWidth(2,200)
        self.ProcessViewT.setColumnWidth(4,300)

        self.NewProcesses.setColumnWidth(3,800)
        self.NewProcesses.setColumnWidth(2,200)
        self.NewProcesses.setColumnWidth(4,300)

        self.ConexionTable.setColumnWidth(4,300)
        self.ConexionTable.setColumnWidth(2,300)

        self.AutoRunTable.setColumnWidth(0,600)
        self.AutoRunTable.setColumnWidth(1,600)

        self.New_process.clicked.connect(self.Page2)
        self.ProcessView.clicked.connect(self.Page1)
        self.RefreshViewProcesses.clicked.connect(self.LoadViewProcess)
        self.RefreshNewProcesses.clicked.connect(self.LoadNewProcess)
        self.CurrentConexions.clicked.connect(self.Page3)
        self.RefreshConexions.clicked.connect(self.LoadConexions)
        self.AutoRun.clicked.connect(self.Page4C)
        self.RefreshAutoRun.clicked.connect(self.LoadAutoRun)
        self.Log_button.clicked.connect(self.ShowLogs)

        self.full_screen = QShortcut(QKeySequence("F11"),self)
        self.full_screen.activated.connect(self.fullscreen)
    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    def LoadAutoRun(self):
        self.AutoRunTable.setRowCount(len(NewAutoRunName))
        num = 0
        for name in NewAutoRunName:
            Curr = CurrentlyRunning[num]
            self.AutoRunTable.setItem(num, 0,QtWidgets.QTableWidgetItem(str(name)))
            self.AutoRunTable.setItem(num, 1,QtWidgets.QTableWidgetItem(str(Curr)))
            num += 1
    def obtener_tiempo_ejecucion(self,pid):
        try:
            proceso = psutil.Process(pid)
            tiempo_ejecucion = datetime.datetime.now() - datetime.datetime.fromtimestamp(proceso.create_time())
            return tiempo_ejecucion
        
        except psutil.NoSuchProcess:
            return "ERROR PID NOT FOUND"

    def LoadConexions(self):
        def Conex():
            conexions = psutil.net_connections()

            self.ConexionTable.setRowCount(len(conexions))
            count = 0
            for conexion in conexions:
                Pid = conexion.pid
                LocalIp = conexion.laddr[0]
                Port = conexion.laddr[1]
                try:
                    RemoteIp = conexion.raddr[0]
                    RemotePort = conexion.raddr[1]
                except:
                    RemoteIp = "N/A"
                    RemotePort = "N/A"
                status = conexion.status
                process = self.GetProcessByPid(Pid)
                self.ConexionTable.setItem(count, 0,QtWidgets.QTableWidgetItem(str(Pid)))
                self.ConexionTable.setItem(count, 1,QtWidgets.QTableWidgetItem(str(process)))
                self.ConexionTable.setItem(count, 2,QtWidgets.QTableWidgetItem(str(LocalIp)))
                self.ConexionTable.setItem(count, 3,QtWidgets.QTableWidgetItem(str(Port)))
                self.ConexionTable.setItem(count, 4,QtWidgets.QTableWidgetItem(str(RemoteIp)))
                self.ConexionTable.setItem(count, 5,QtWidgets.QTableWidgetItem(str(RemotePort)))
                self.ConexionTable.setItem(count, 6,QtWidgets.QTableWidgetItem(str(status)))
                count += 1
        messagebox.showwarning("Please wait until we get all conexion","Please wait until we get all conexion")
        th2 = threading.Thread(target=Conex)
        th2.start()
    def GetProcessByPid(self,pid):
        for process in psutil.process_iter():
            if process.pid == pid:
                return process.name()

        return None    
    def Page1(self):
        self.Pages.setCurrentIndex(0)    
    def Page2(self):
        self.Pages.setCurrentIndex(1)
    def Page3(self):
        self.Pages.setCurrentIndex(2)
    def Page4C(self):
        self.Pages.setCurrentIndex(3)
    def ShowLogs(self):
        try:
            current = os.getcwd()
            Full = os.path.join(current,"Logs.txt")
            os.system(f"notepad.exe {Full}")
        except:
            messagebox.showerror("Can't open log file")
    def LoadNewProcess(self):
        def Processess():
            count =0 
            for process in NewProcessName:
                count += 1
            self.NewProcesses.setRowCount(count)
            count = 0
            for process in NewProcessName:
                PID = NewProcessPID[count]
                MemUsage = NewProcessMemUsage[count]
                CMDLine = NewProcessCmdLine[count]
                ProcessRunTime = NewProcessRunTime[count]
                self.NewProcesses.setItem(count, 0,QtWidgets.QTableWidgetItem(str(PID)))
                self.NewProcesses.setItem(count, 1,QtWidgets.QTableWidgetItem(process))
                self.NewProcesses.setItem(count, 2,QtWidgets.QTableWidgetItem(str(ProcessRunTime)))
                self.NewProcesses.setItem(count, 3,QtWidgets.QTableWidgetItem(str(CMDLine)))
                self.NewProcesses.setItem(count, 4,QtWidgets.QTableWidgetItem(str(MemUsage)))
                
                count += 1
        th3 = threading.Thread(target=Processess)
        th3.start()

    def LoadViewProcess(self):
        def ViewProcesses():
            row = 0
            count = 0
            for proc in psutil.process_iter():
                count += 1
            self.ProcessViewT.setRowCount(count)
            for process in psutil.process_iter():
                tiempo_ejecucion = self.obtener_tiempo_ejecucion(process.pid)
                self.ProcessViewT.setItem(row, 0,QtWidgets.QTableWidgetItem(str(process.pid)))
                self.ProcessViewT.setItem(row, 1,QtWidgets.QTableWidgetItem(process.name()))
                self.ProcessViewT.setItem(row, 2,QtWidgets.QTableWidgetItem(str(tiempo_ejecucion)))

                
                try:
                    cmd = process.cmdline()
                except:
                    cmd = "ACCESS DENIED"
                self.ProcessViewT.setItem(row, 3,QtWidgets.QTableWidgetItem(str(cmd)))
                memory_percent = f"{round(process.memory_percent(),2)}%"
                self.ProcessViewT.setItem(row, 4,QtWidgets.QTableWidgetItem(str(memory_percent)))
                row += 1
        th = threading.Thread(target=ViewProcesses)
        th.start()
    def OpenDiscord(self):
        def open():
            os.system(f"start https://discord.gg/7vppDTAu")
        thread1 = threading.Thread(target=open)
        thread1.start()
namePrograms = []
Path = []
AlreadyFinded = []
def obtener_tiempo_ejecucion(pid):
        try:
            proceso = psutil.Process(pid)
            tiempo_ejecucion = datetime.datetime.now() - datetime.datetime.fromtimestamp(proceso.create_time())
            return tiempo_ejecucion
        
        except psutil.NoSuchProcess:
            return "ERROR PID NOT FOUND"
def listar_tareas_programadas():
    try:
        program = []
        Routes=  []
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        task_collection = root_folder.GetTasks(0)

        for i in range(0, task_collection.Count):
            task = task_collection.Item(i+1)
            program.append(task.Name)
            Routes.append(task.Path)

        return program, Routes
    except Exception as e:
            with open("Logs.txt","a") as file:
                file.write(f'''
                           
Exception ERROR: {str(e)}
''')

def createNotification(titulo, mensaje,tiempo_mostrado=10):
    notification.notify(
    title=titulo,
    message=mensaje,
    timeout=tiempo_mostrado
    )

def CheckForNewAutoRuns():
    while True:
        Programs,Routes = obtener_programas_inicio()
        Program, Route = listar_tareas_programadas()

        Final_Programs,Final_Routes = Programs + Program, Routes + Route
        num = 0
        result = [elemento for sublist in namePrograms for elemento in sublist]
        try:

            for element in Final_Programs:
                if element not in result and element not in AlreadyFinded:
                    AlreadyFinded.append(element)
                    finded = False
                    for process in psutil.process_iter():
                        if process.name().lower() == element.lower():
                            
                            toast("NEW STARTUP APPLICATION",f"NEW STARTUP APPLICATION DETECTED: {element} CURRENTLY RUNNING AS :{process.name()} WITH PID: {process.pid}")
                            finded = True
                            CurrentlyRunning.append(True)

                    if finded == False:
                        toast("NEW STARTUP APPLICATION",f"NEW STARTUP APPLICATION DETECTED: {element} IS NOT CURRENTLY RUNNING IN THE SYSTEM")
                        CurrentlyRunning.append(False)
                    
                    NewAutoRunName.append(element)
                    

                    result.append(element)

                    time.sleep(1)
        except Exception as e:
            with open("Logs.txt","a") as file:
                file.write(f'''
                           
Exception ERROR: {str(e)}
''')

def getProcesses():
    Processes = {}
    for process in psutil.process_iter():
        if process.name() in Processes:
            Processes[process.name()] += 1
        else:
            Processes[process.name()] = 0


    return Processes

def DetectNewProcesses():
    th32Screenshot = getProcesses()
    try:

        if th32Screenshot:
            newProc = {}
            while True:
                for process in psutil.process_iter():
                    if process.name() not in th32Screenshot:
                        NewProcessName.append(process.name())
                        NewProcessPID.append(process.pid)
                        memory_percent = f"{round(process.memory_percent(),2)}%"
                        NewProcessMemUsage.append(memory_percent)
                        try:
                            cmd = process.cmdline()
                        except:
                            cmd = "N/A"

                        NewProcessCmdLine.append(cmd)
                        NewProcessRunTime.append(obtener_tiempo_ejecucion(process.pid))

                        th32Screenshot[process.name()] = 0

                        toast(f"NEW PROCESS DETECTED!! : {process.name()} CURRENTLY RUNNING WITH PID : {process.pid}")
                        
                        
                    if process.name() in newProc:
                        newProc[process.name()] += 1
                    else:
                        newProc[process.name()] = 0
    except Exception as e:
            with open("Logs.txt","a") as file:
                file.write(f'''
                           
Exception ERROR: {str(e)}
''')

def obtener_programas_inicio():
    Programs = []
    Routes = []
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        start_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path)

        for i in range(winreg.QueryInfoKey(start_key)[1]):
            program_name, program_path = winreg.EnumValue(start_key, i)[:2]
            Programs.append(program_name)
            Routes.append(program_path)

        winreg.CloseKey(start_key)
        return Programs,Routes
    except WindowsError as e:
        messagebox.showerror("ERROR MESSAGE",f"ERROR COULDN'T OPEN REGISTRY KEY FOR SEARCH AUTORUNS!!! ERROR TYPE: {str(e)}")
num = 0


if __name__ == "__main__":
    if platform.system() != "Windows":
        messagebox.showerror("ONLY WINDOWS SUPPORTED",f"ONLY WINDOWS SUPPORTED")
    if os.path.exists("UI.ui"):
        pass
    else:
        messagebox.showwarning("UI.ui is not installed","UI.ui IS NOT INSTALLED, GONNA DOWNLOAD!")
        time.sleep(1)
    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        messagebox.showwarning("PROGRAM IS NOT RUNNING WITH ADMINISTRATOR","PROGRAM IS NOT RUNNING WITH ADMINISTRATOR, SOME FEARURES ARE NOT ENABLED!")
    Programs,Routes = obtener_programas_inicio()
    Program, Route = listar_tareas_programadas()

    Final_Programs,Final_Routes = Programs + Program, Routes + Route

    namePrograms.append(Final_Programs)
    Path.append(Final_Routes)

    try:

        Thread1 = threading.Thread(target=CheckForNewAutoRuns)
        Thread1.start()

        Thread2 = threading.Thread(target=DetectNewProcesses) 
        Thread2.start()
    except Exception as e:
        with open("Logs.txt","a") as file:
            file.write(f'''
                        
Exception ERROR: {str(e)}
''')
    
    app = QApplication(sys.argv)
    GUI = MainUI()
    GUI.setWindowTitle("CONTROL CENTER")
    GUI.show()
    
    sys.exit(app.exec_())
