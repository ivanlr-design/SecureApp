import psutil

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

def DetectNewConexions():
    Pid, LocalIp, LocalPort, RemoteIp, RemotePort, Status = GetAllConexions()

    while True:
        for conexion in psutil.net_connections():
            if conexion.pid not in Pid:
                print("NEW CONEXION: ", conexion.pid)
DetectNewConexions()