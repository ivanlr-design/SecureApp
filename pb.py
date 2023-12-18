import wmi
w = wmi.WMI(namespace="root\wmi")
print((w.MSAcpi_ThermalZoneTemperature()[0].CurrentTemperature / 10.0)-273.15)