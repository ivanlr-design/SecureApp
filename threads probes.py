import psutil
import os
import time
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
                print(proces,Threads_ant,Threads_desp)
                if Threads_ant != Threads_desp:
                    new_threads = Threads_ant - Threads_desp
                    
                    print(f"NEW THREAD : {proces} -> {new_threads}")
                    if Threads_ant > Threads_desp:
                        major = Threads_ant
                    else:
                        major = Threads_desp
                    change = True
                    
                    time.sleep(20)

        if change == True:
            Processos[process] = major
            procesos[process] = major
                    


DetectNewThreads()