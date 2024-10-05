"""
This bit of script just lists serial ports.
I know, surprising. But useful sometimes.
"""
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f'{port}')
