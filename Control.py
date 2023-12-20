import winreg
import win32com.client
import requests
import wmi
import os
import ctypes
import subprocess
import win32com.client
import re
import time
import platform
import locale
import datetime
import sys
import threading
from win11toast import toast
from tkinter import messagebox
import signal
import psutil
from subprocess import PIPE
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

Threads = True
AutoRun = True
Processes = True
closed = False
DetectConexions = True
RunInBackground = True

NewConexionLocalIp = []
NewConexionLocalPort = []
NewConexionRemoteIp = []
NewConexionRemotePort = []
NewConexionStatus = []
NewConexionPid = []

class MainUI(QMainWindow):
    def __init__(self):
        self.AllSsids = False
        super(MainUI,self).__init__()
        self.setWindowTitle("MAIN CONTROL CENTER")
        uic.loadUi("UI.ui",self)
        self.showFullScreen()
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
        
        self.SystemTable.setColumnWidth(0,200)
        self.SystemTable.setColumnWidth(1,300)
        self.SystemTable.setColumnWidth(2,300)
        self.SystemTable.setColumnWidth(3,300)

        self.WifiTable.setColumnWidth(0,200)
        self.WifiTable.setColumnWidth(1,300)
        self.WifiTable.setColumnWidth(2,300)
        self.WifiTable.setColumnWidth(3,300)
        self.WifiTable.setColumnWidth(4,300)


        self.New_process.clicked.connect(self.Page2)
        self.ProcessView.clicked.connect(self.Page1)
        self.RefreshViewProcesses.clicked.connect(self.LoadViewProcess)
        self.RefreshNewProcesses.clicked.connect(self.LoadNewProcess)
        self.CurrentConexions.clicked.connect(self.Page3)
        self.RefreshConexions.clicked.connect(self.LoadConexions)
        self.AutoRun.clicked.connect(self.Page4C)
        self.RefreshAutoRun.clicked.connect(self.LoadAutoRun)
        self.Log_button.clicked.connect(self.ShowLogs)
        self.Monitor.clicked.connect(self.Page5)
        self.System.clicked.connect(self.Page6)
        self.PID.returnPressed.connect(self.kill_process_by_pid)
        self.Wifi_button.clicked.connect(self.Wifi_Page)
        self.NewConexions.clicked.connect(self.ConexionPage)
        self.WifiSelection.currentIndexChanged.connect(self.UpdateWifiTable)

        self.WifiCheckBox.clicked.connect(self.UpdateCheckBox)
        self.NewAutoRunCheckBox.clicked.connect(self.ConfigAutoRun)
        self.NewProcessesCheckBox.clicked.connect(self.ConfigNewProcesses)
        self.ThreadCheckBox.clicked.connect(self.ConfigThread)
        self.Background.clicked.connect(self.ConfigBackground)
        self.Conexions.clicked.connect(self.ConfigConexion)
        self.RefreshNewConexions.clicked.connect(self.UpdateNewConexionTable)
        self.Background.setChecked(True)
        self.NewAutoRunCheckBox.setChecked(True)
        self.NewProcessesCheckBox.setChecked(True)
        self.ThreadCheckBox.setChecked(True)
        self.Conexions.setChecked(True)

        self.WifiLineEdit.returnPressed.connect(self.UpdateWifiLineStatus)
        self.ConfigButton.clicked.connect(self.ConfigPageSelector)
        self.full_screen = QShortcut(QKeySequence("F11"),self)
        self.full_screen.activated.connect(self.fullscreen)
        try:
            user = os.getlogin()
        except:
            user = "Uknown user"
        try:
            path = os.getcwd()
        except:
            path = "N/A"
        
        
        self.UpdateWifiStatus()

        self.UserLabel.setText(f"Current User : {user}")
        self.CurrentPath.setText(f"Current Path : {path}")
        th3 = threading.Thread(target=self.UploadSystemTable)
        th3.start()

    def ConfigConexion(self):
        global DetectConexions
        if self.Conexions.isChecked():
            DetectConexions = True
        else:
            DetectConexions = False

    def ConfigBackground(self):
        pass
    
    def closeEvent(self,event):
        global closed, RunInBackground
        closed = True
        if self.Background.isChecked():
            toast("APP WILL RUN IN BACKGROUND","APP WILL RUN IN BACKGROUND")
        else:
            RunInBackground = False
            Thread1.join()
            Thread2.join()
            Thread3.join()
        event.accept()
        

    def ConfigThread(self):
        global Threads
        if self.ThreadCheckBox.isChecked():
            Threads = True
        else:
            Threads = False

    def ConfigNewProcesses(self):
        global Processes
        if self.NewProcessesCheckBox.isChecked():
            Processes = True
        else:
            Processes = False

    def ConfigAutoRun(self):
        global AutoRun
        if self.NewAutoRunCheckBox.isChecked():
            AutoRun = True
        else:
            AutoRun = False


    def UpdateCheckBox(self):
        if self.WifiCheckBox.isChecked():
            Net = Networking()
            SSIDS = Net.GetWifiList()
            if SSIDS:
                self.WifiTable.setRowCount(len(SSIDS))
                row = 0
                for SSID in SSIDS:
                    Password,Autentication,Cipher,Mac = Net.GetWifiPasswordBySSID(SSID)
                    self.WifiTable.setItem(row, 0,QtWidgets.QTableWidgetItem(str(SSID)))
                    self.WifiTable.setItem(row, 1,QtWidgets.QTableWidgetItem(str(Password)))
                    self.WifiTable.setItem(row, 2,QtWidgets.QTableWidgetItem(str(Mac)))
                    self.WifiTable.setItem(row, 3,QtWidgets.QTableWidgetItem(str(Cipher)))
                    self.WifiTable.setItem(row, 4,QtWidgets.QTableWidgetItem(str(Autentication)))
                    row +=1
                    
                self.AllSsids = True
           
            else:
                self.WifiCheckBox.setChecked(False)
                messagebox.showwarning("WIFI WARNING","CAN'T GET WIFI SSIDS")
            
        else:
            self.AllSsids = False

    def UpdateWifiLineStatus(self):
        if self.AllSsids == False:
            self.WifiTable.setRowCount(1)
            text = self.WifiLineEdit.text()
            Net = Networking()
            try:
                Password,Autentication,Cipher,Mac = Net.GetWifiPasswordBySSID(text)
                if Password:
                    self.WifiTable.setItem(0, 0,QtWidgets.QTableWidgetItem(str(text)))
                    self.WifiTable.setItem(0, 1,QtWidgets.QTableWidgetItem(str(Password)))
                    self.WifiTable.setItem(0, 2,QtWidgets.QTableWidgetItem(str(Mac)))
                    self.WifiTable.setItem(0, 3,QtWidgets.QTableWidgetItem(str(Cipher)))
                    self.WifiTable.setItem(0, 4,QtWidgets.QTableWidgetItem(str(Autentication)))
                else:
                    messagebox.showwarning("INVALID SSID PROVIDED",f"INVALID SSID PROVIDED : {text}")
                
            except Exception as e:
                with open("Logs.txt","a") as file:
                    file.write(f"\n(ERROR IN FUNCTION UPDATEWIFILINESTATUS ) - TYPE ERROR : {str(e)}")

    def UpdateWifiTable(self,index):
        if self.AllSsids == False:
            text = self.WifiSelection.currentText()
            self.WifiTable.setRowCount(1)
            Net = Networking()
            Password,Autentication,Cipher,Mac = Net.GetWifiPasswordBySSID(text)
            self.WifiTable.setItem(0, 0,QtWidgets.QTableWidgetItem(str(text)))
            self.WifiTable.setItem(0, 1,QtWidgets.QTableWidgetItem(str(Password)))
            self.WifiTable.setItem(0, 2,QtWidgets.QTableWidgetItem(str(Mac)))
            self.WifiTable.setItem(0, 3,QtWidgets.QTableWidgetItem(str(Cipher)))
            self.WifiTable.setItem(0, 4,QtWidgets.QTableWidgetItem(str(Autentication)))
        
    def UpdateNewConexionTable(self):
        rows = len(NewConexionLocalIp)

        self.NewConexionTable.setRowCount(rows)

        row = 0
        for LocalIp in NewConexionLocalIp:
            pid = NewConexionPid[row]
            Procname = self.GetProcessByPid(pid)
            LocalPort = NewConexionLocalPort[row]
            RemoteIp = NewConexionRemoteIp[row]
            RemotePort = NewConexionRemotePort[row]
            Status = NewConexionStatus[row]
            self.NewConexionTable.setItem(row, 0,QtWidgets.QTableWidgetItem(str(pid)))
            self.NewConexionTable.setItem(row, 1,QtWidgets.QTableWidgetItem(str(Procname)))
            self.NewConexionTable.setItem(row, 2,QtWidgets.QTableWidgetItem(str(LocalIp)))
            self.NewConexionTable.setItem(row, 3,QtWidgets.QTableWidgetItem(str(LocalPort)))
            self.NewConexionTable.setItem(row, 4,QtWidgets.QTableWidgetItem(str(RemoteIp)))
            self.NewConexionTable.setItem(row, 5,QtWidgets.QTableWidgetItem(str(RemotePort)))
            self.NewConexionTable.setItem(row, 6,QtWidgets.QTableWidgetItem(str(Status)))
            row += 1
            


    def UpdateWifiStatus(self):
        Net = Networking()
        SSIDS = Net.GetWifiList()
        self.WifiSelection.addItems(SSIDS)

       
    def UploadSystemTable(self):
        self.SystemTable.setRowCount(1)
        while True:
            if RunInBackground == False:
                break
            systemcalls = psutil.cpu_stats().syscalls
            cpu_freq_max = psutil.cpu_freq().max
            cpu_freq_current = psutil.cpu_freq().current
            try:
                w = wmi.WMI(namespace="root\wmi")
                CurrentTemperature = ((w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10.0)-273.15) 
                CurrentTemperature = f"{CurrentTemperature}°C"
            except:
                CurrentTemperature = "ACCESS DENIED ERROR"
            self.SystemTable.setItem(0, 0,QtWidgets.QTableWidgetItem(str(systemcalls)))
            self.SystemTable.setItem(0, 1,QtWidgets.QTableWidgetItem(str(cpu_freq_current)))
            self.SystemTable.setItem(0, 2,QtWidgets.QTableWidgetItem(str(cpu_freq_max)))
            self.SystemTable.setItem(0, 3,QtWidgets.QTableWidgetItem(str(CurrentTemperature)))
            time.sleep(1)

    def kill_process_by_pid(self):
        Pid = self.PID.text()
        Pid = str(Pid).strip()
        try:
            Pid = int(Pid)
            finded = False
            for process in psutil.process_iter():
                if process.pid == Pid:
                    try:
                        os.kill(process.pid,signal.SIGTERM)
                        messagebox.showinfo(f"Process killed",f"Process named : {process.name()} with PID : {process.pid} was killed")
                    except Exception as e:
                       messagebox.showerror(f"Failed to kill process",f"FAILED TO KILL PROCESS NAMED : {process.name()} with PID : {process.pid} ERROR TYPE : {str(e)}")
                    finded = True
                
            if finded == False:
                messagebox.showwarning("PROCESS",F"PROCESS WITH PID : {Pid} WASN'T FINDED")
        except: 
            messagebox.showwarning("PID IS A NUMBER, NO NUMBER WAS PROVIDED","PID IS A NUMBER, NO NUMBER WAS PROVIDED")
        
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
    def Page5(self):
        self.Pages.setCurrentIndex(4)
    def Page6(self):
        self.Pages.setCurrentIndex(5)
    def Wifi_Page(self):
        self.Pages.setCurrentIndex(6)
    def ConfigPageSelector(self):
        self.Pages.setCurrentIndex(7)
    def ConexionPage(self):
        self.Pages.setCurrentIndex(8)
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
    

class Networking():
    def __init__(self) -> None:
        pass
    
    def GetWifiPasswordBySSID(self,SSID):
        cmd = subprocess.Popen(f'netsh wlan show profiles "{SSID}" key=clear ',shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        cmd.wait()
        Password = []
        Mac = []
        Autentication = []
        Cipher = []

        patron_clave_esp = re.compile(r'Contenido de la clave\s+:\s+([^\n]+)')
        patron_clave_eng = re.compile(r'Key Content\s+:\s+([^\n]+)')
        patron_clave_aleman = re.compile(r'Schlüsselinhalt\s+:\s+([^\n]+)')

        patron_Mac_esp = re.compile(r'Selecci¢n aleatoria de direcci¢n MAC:\s+(.*)')
        patron_Mac_eng = re.compile(r'Random MAC address selection:\s+(.*)', re.IGNORECASE)
        patron_Mac_aleman = re.compile(r'Zufällige MAC-Adressauswahl:\s+(.*)', re.IGNORECASE)

        patron_Aut_esp = re.compile(r'Autenticaci¢n\s*:\s*(.*)', re.IGNORECASE)
        patron_Aut_eng = re.compile(r'Authentication\s*:\s*(.*)', re.IGNORECASE)
        patron_Aut_aleman = re.compile(r'Authentifizierung\s*:\s*(.*)', re.IGNORECASE)

        patron_cipher_esp = re.compile(r'Cifrado\s*:\s*(.*)', re.IGNORECASE)
        patron_cipher_eng = re.compile(r'Encryption\s*:\s*(.*)', re.IGNORECASE)
        patron_cipher_aleman = re.compile(r'Verschlüsselung\s*:\s*(.*)', re.IGNORECASE)
        patron = re.compile(r'(Random MAC address selection|Selección aleatoria de dirección MAC|Zufällige MAC-Adressauswahl):\s+(enabled|disabled)')
        if cmd.returncode == 0:
            output = cmd.stdout.read().decode('latin-1',errors='replace')
            if patron_clave_esp.search(output):
                password = patron_clave_esp.search(output).group(1).strip()
                Password.append(password)
            elif patron_clave_eng.search(output):
                password = patron_clave_eng.search(output).group(1).strip()
                Password.append(password)
            elif patron_clave_aleman.search(output):
                password = patron_clave_aleman.search(output).group(1).strip()
                Password.append(password)
            
            if patron_Mac_esp.search(output):
                Seleccion = patron_Mac_esp.search(output).group(1).strip()
                Mac.append(Seleccion)
            elif patron_Mac_eng.search(output):
                Seleccion = patron_clave_eng.search(output).group(1).strip()
                Mac.append(Seleccion)
            elif patron_Mac_aleman.search(output):
                Seleccion = patron_Mac_aleman.search(output).group(1).strip()
                Mac.append(Seleccion)

            if patron_Aut_esp.search(output):
                Aut = patron_Aut_esp.search(output).group(1).strip()
                Autentication.append(Aut)
            elif patron_Aut_eng.search(output):
                Aut = patron_Aut_eng.search(output).group(1).strip()
                Autentication.append(Aut)
            elif patron_Aut_aleman.search(output):
                Aut = patron_Aut_aleman.search(output).group(1).strip()
                Autentication.append(Aut)
            
            if patron_cipher_esp.search(output):
                Cip = patron_cipher_esp.search(output).group(1).strip()
                Cipher.append(Cip)
            elif patron_cipher_eng.search(output):
                Cip = patron_cipher_eng.search(output).group(1).strip()
                Cipher.append(Cip)
            elif patron_cipher_aleman.search(output):
                Cip = patron_cipher_aleman.search(output).group(1).strip()
                Cipher.append(Cip)

            else:
                with open("Logs.txt","a") as file:
                    file.write(f"\n(GetWifiPasswordBySSID function) - Can't get password by netsh command (Can't get password)!\n")
        else:
            with open("Logs.txt","a") as file:
                file.write(f"\n(GetWifiPasswordBySSID function) - Can't get password by netsh command (returncode error)!\n")
                
        if len(Password) == 0:
            Password.append("N/A")
        if len(Autentication) == 0:
            Autentication.append("N/A")
        if len(Cipher) == 0:
            Cipher.append("N/A")
        if len(Mac) == 0:
            Mac.append("N/A")
        return Password[0],Autentication[0],Cipher[0],Mac[0]


    def GetWifiList(self):
        cmd = subprocess.Popen("netsh wlan show profiles",shell=True,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        full_line = 8
        cmd.wait()
        SSID = []
        try:
            cmd = cmd.stdout.read().decode(errors="replace")
        except:
            with open("Logs.txt","a") as file:
                file.write(F"\n(GetWifiList function) - CAN'T GET SSIDS FROM NETSH COMMAND!\n")

        if cmd:
            splited = cmd.split("\n")
            full_command = []
            num = 0
            for line in splited:
                if num > full_line:
                    full_command.append(line)
                num += 1
            
            for wifi in full_command:
                try:
                    SSID.append(wifi.split(":")[1].strip())
                except Exception as e:
                    with open("Logs.txt","a") as file:
                        file.write(f"ERROR TYPE IN GET ALL SSID FUNCTION : {str(e)}\n")


        return SSID



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
        if RunInBackground == False:
            break
        if AutoRun == True:
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
                if RunInBackground == False:
                    break
                if Processes == True:
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
def Download():
    s = requests.get("https://raw.githubusercontent.com/ivanlr-design/SecureApp/main/UI.ui")
    if s.status_code == 200:
        return s.text
    else:
        messagebox.showerror("Failed To download")
        sys.exit(1)

def ObtainThreads():
    procesos = {}
    for process in psutil.process_iter():
        if process.name() in procesos:
            procesos[process.name()] += 1
        else:
            procesos[process.name()] = 0

    return procesos

def DetectNewThreads():
    Processos = ObtainThreads()
    
    while True:
        if Threads == True:
            if RunInBackground == False:
                break

            change = False
            procesos = {}
            for process in psutil.process_iter():

                if process.name() in procesos:
                    procesos[process.name()] += 1
                else:
                    procesos[process.name()] = 0

            for proces in procesos:
                if proces in Processos:
                    
                    Threads_ant = Processos.get(proces)
                    Threads_desp = procesos.get(proces)
                    if Threads_ant != Threads_desp:
                        new_threads = Threads_desp - Threads_ant
                        
                        toast("THREADS HANDLER",f"NEW THREAD : {proces} -> {new_threads}")
                        if Threads_ant > Threads_desp:
                            major = Threads_ant
                        else:
                            major = Threads_desp
                        change = True
                        
                        time.sleep(20)

            if change == True:
                Processos[process] = major
                procesos[process] = major
                        

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

class WindowsUpdateChecker:
    def __init__(self):
        self.update_session = win32com.client.Dispatch('Microsoft.Update.Session')

    def get_pending_updates(self):
        search_result = self.update_session.CreateUpdateSearcher().Search('IsInstalled=0')
        updates = search_result.Updates

        pending_updates = []
        for update in updates:
            pending_updates.append({
                'Title': update.Title,
                'Description': update.Description,
                'KB': update.KBArticleIDs[0] if update.KBArticleIDs else 'N/A'
            })

        return pending_updates

def GetAllConexions():
    Pid = []
    LocalIp = []
    LocalPort = []
    RemoteIp = []
    RemotePort = []
    Status = []
    for conexion in psutil.net_connections():
        Pid.append(conexion.pid)
        LocalIp.append(conexion.laddr[0])
        LocalPort.append(conexion.laddr[1])
        try:
            RemoteIp.append(conexion.raddr[0])
        except:
            RemoteIp.append("Unknown")
        try:
            RemotePort.append(conexion.raddr[1])
        except:
            RemotePort.append("Unknown")

        
        Status.append(conexion.status)

    return Pid, LocalIp, LocalPort, RemoteIp, RemotePort, Status

def GetProcessByPid(Pid):
    for process in psutil.process_iter():
        if int(process.pid) == int(Pid):
            return process.name()
        
    return False

def DetectNewConexions():
    Pid, LocalIp, LocalPort, RemoteIp, RemotePort, Status = GetAllConexions()

    while True:
        if DetectConexions == True:
            
            for conexion in psutil.net_connections():
                if conexion.pid not in Pid:
                    try:
                        RIp = conexion.raddr[0]
                        Port = conexion.raddr[1]
                    except:
                        RIp = "Unknown"
                        Port = "Unknow"

                    NewConexionLocalIp.append(conexion.laddr[0])
                    NewConexionLocalPort.append(conexion.laddr[1])
                    NewConexionRemoteIp.append(RIp)
                    NewConexionRemotePort.append(Port)
                    NewConexionPid.append(conexion.pid)
                    NewConexionStatus.append(conexion.status)

                    ProcessName = GetProcessByPid(conexion.pid)
                    toast("NEW CONEXION DETECTED",F"NEW CONEXION DETECTED FROM REMOTE : {RIp}:{Port} ({conexion.pid}-{ProcessName}) LOCAL : {conexion.laddr[0]}:{conexion.laddr[1]} STATUS : {conexion.status}")
                    Pid.append(conexion.pid)
if __name__ == "__main__":
    supported_languages = ["es","en","de"]
    if platform.system() != "Windows":
        messagebox.showerror("ONLY WINDOWS SUPPORTED",f"ONLY WINDOWS SUPPORTED")
    if os.path.exists("UI.ui"):
        pass
    else:
        messagebox.showwarning("UI.ui is not installed","UI.ui IS NOT INSTALLED, GONNA DOWNLOAD!")
        re = Download()
        if re:
            with open("UI.ui","w") as file:
                file.write(re)
        time.sleep(1)

    if ctypes.windll.shell32.IsUserAnAdmin():
        pass
    else:
        messagebox.showwarning("PROGRAM IS NOT RUNNING WITH ADMINISTRATOR","PROGRAM IS NOT RUNNING WITH ADMINISTRATOR, SOME FEARURES ARE NOT ENABLED!")
    
    lang = locale.getlocale()[0]
    for language in supported_languages:
        language = language.split("_")[0]
        lang = lang.split("_")[0]
        if language == lang:
            break
        else:
            messagebox.showwarning(f"LANGUAGE WARNING","YOUR SYSTEM LANGUAGE IS NOT SUPPORTED IN THIS APP, SOME FEATURES MAY NOT WORK RIGHT!")

    checker = WindowsUpdateChecker()
    pending_updates = checker.get_pending_updates()

    try:
        if pending_updates:
            for update in pending_updates:

                messagebox.showwarning("WINDOWS UPDATE WAS DETECTED!",f"Windows Update\nTitle : {update['Title']}\nDescription : {update['Description']}\nKB Update : {update['KB']}")
        else:
            pass
    except Exception as e:
        with open("Logs.txt","a") as file:
            file.write(f'''
                        
Exception ERROR: {str(e)}
''')


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

        Thread3 = threading.Thread(target=DetectNewThreads) 
        Thread3.start()

        Thread4 = threading.Thread(target=DetectNewConexions)
        Thread4.start()
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

