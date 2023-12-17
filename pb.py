import psutil

conexions = psutil.net_connections()

for conex in conexions:
    print(conex)