import winreg

# Ruta al registro de inicio automático actual del usuario actual
ruta_autostart = r"Software\Microsoft\Windows\CurrentVersion\Run"

# Nombre y ruta del programa que quieres agregar al inicio automático
nombre_programa = "MiPrograma"
ruta_programa = r"C:\Users\portatil\Downloads\SysInfoSiu.exe"

try:
    # Abrir la clave del registro para el inicio automático
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, ruta_autostart, 0, winreg.KEY_WRITE)

    # Crear una nueva clave en el registro para tu programa
    winreg.SetValueEx(key, nombre_programa, 0, winreg.REG_SZ, ruta_programa)

    # Cerrar la clave del registro
    winreg.CloseKey(key)

    print(f"Se agregó '{nombre_programa}' a las aplicaciones de inicio automático.")

except Exception as e:
    print(f"Ocurrió un error: {e}")
