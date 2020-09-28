import serial
import serial.tools.list_ports
import json

port_list = list(serial.tools.list_ports.comports())
for i in port_list:
    print(list(i))
ser = serial.Serial('COM3',1200)#設定要監聽哪一個port和baud rate

def readCOM(ser):
    while(1):
        check = ser.read(1)
        check = check.decode('utf-8')
        print("check = ",check)
readCOM(ser)
while(1):
    pass
