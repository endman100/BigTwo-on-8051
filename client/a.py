import serial
import serial.tools.list_ports
import json
from selenium import webdriver

browser = webdriver.Chrome("./chromedriver.exe")  #開啟網頁模擬器
browser.get("http://10.27.4.8:7777")  #連線目標網頁
port_list = list(serial.tools.list_ports.comports())
for i in port_list:
    print(list(i))
ser = serial.Serial('COM8',1200)#設定要監聽哪一個port和baud rate

def readCOM(ser):
    while(1):
        check = ser.read(1)
        check = check.decode('utf-8')
        print("check = ",check,type(check))

        if(check == 'D'):
            browser.execute_script("fakeSendData();return 1;")
        if(check == 'A'):
            browser.execute_script("addCard(10);return 1;")
        if(check == 'B'):
            browser.execute_script("addCard(11);return 1;")
        if(check == 'C'):
            browser.execute_script("addCard(12);return 1;")
        if(check == '1'):
            browser.execute_script("addCard(1);return 1;")
        if(check == '2'):
            browser.execute_script("addCard(2);return 1;")
        if(check == '3'):
            browser.execute_script("addCard(3);return 1;")
        if(check == '4'):
            browser.execute_script("addCard(4);return 1;")
        if(check == '5'):
            browser.execute_script("addCard(5);return 1;")
        if(check == '6'):
            browser.execute_script("addCard(6);return 1;")
        if(check == '7'):
            browser.execute_script("addCard(7);return 1;")
        if(check == '8'):
            browser.execute_script("addCard(8);return 1;")
        if(check == '9'):
            browser.execute_script("addCard(9);return 1;")
        if(check == '0'):
            browser.execute_script("addCard(0);return 1;")
readCOM(ser)
while(1):
    pass
