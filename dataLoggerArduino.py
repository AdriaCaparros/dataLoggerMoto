import time
import os
import can
import math


VEHICLE_SPEED = 0x80
VOLTAGE_BATTERY = 0x274
TEMP1= 0x195
TEMP2=0x146
TEMP3=0x168
TEMP4=0x370
SOC_BATTERY=0xA0
RPM=0xA1

os.remove("/media/pi/AFEC-4877/log.txt")
outfile=open('/media/pi/AFEC-4877/log.txt','w')


print('\n\rCAN Rx test')
print('Bring up CAN0...')

#Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 down")
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Ready')
bus = can.interface.Bus(channel='can0',bustype='socketcan_native')

arduino_1 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x2F)
arduino_2 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x3F)


voltage=0
corrent=0
corrent_maxim=0
temperatura_motor=0
temperatura_inversor=0
velocitat=0
revolucions=0
accelerador=0
temp1=0
c=''
count=0
valor=0



while True:
    for j in range(4):
        message = bus.recv(timeout=1.0)
        if message is not None:
            c='{0:f},{1:d},'.format(message.timestamp,count)
            valor=0
            print("Id: ", message.arbitration_id)
            print("Valor: ", message.data)
            if(message.arbitration_id==0x2F):
                print("Id: ", message.arbitration_id)
                arduino_1.data = message.data
                valor=arduino_1.data
                print("Valor arduino 1: ",valor)
