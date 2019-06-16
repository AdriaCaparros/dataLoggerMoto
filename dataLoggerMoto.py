
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

tpdo_1 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x274)
tpdo_2 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x195)
tpdo_3 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x146)
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
            if (message.arbitration_id == 0x274):
                print("Id: ", message.arbitration_id)
                tpdo_1.data = message.data
                # TPDO1 ---------------------------------------
                # VOLTATGE BATERIA (V)
                valor = tpdo_1.data[1]
                valor = (valor << 8) | tpdo_1.data[0]  # Traiem el valor del missatge
                voltatge = valor * 0.0625  # Apliquem el factor de multiplicació
                print("Voltatge: ",voltatge)
                # CORRENT BATERIA (A)
                valor = tpdo_1.data[3]
                valor = (valor << 8) | tpdo_1.data[2]  # Traiem el valor del missatge
                corrent = valor * 0.0625  # Apliquem el factor de multiplicació
                print("Corrent: ", corrent)
                # CORRENT MAXIM DESCARREGA BATERIA (A)
                valor = tpdo_1.data[5]
                corrent_maxim = (valor << 8) | tpdo_1.data[4]  # Traiem el valor del missatge
                print("Corren maxim: ", corrent_maxim)
            if (message.arbitration_id== 0x195):
                print("Id: ", message.arbitration_id)
                tpdo_2.data = message.data
                # TPDO2 ---------------------------------------
                # TEMPERATURA MOTOR (ºC)
                valor = tpdo_2.data[1]
                temperatura_motor = (valor << 8) | tpdo_2.data[0]  # Traiem el valor del missatge
                print("Temperatura motor: ", temperatura_motor)
                # TEMPERATURA INVERSOR (ºC)
                temperatura_inversor = tpdo_2.data[2]  # Traiem el valor del missatge
                print("Temperatura inversor: ", temperatura_inversor)
            if (message.arbitration_id==0x146):
                print("Id: ", message.arbitration_id)
                tpdo_3.data = message.data
                # TPDO3 ---------------------------------------
                # VELOCITAT DEL VEHICLE (kph)
                valor = tpdo_3.data[1]
                valor = (valor << 8) | tpdo_3.data[0]  # Traiem el valor del missatge
                velocitat = valor * 0.0625  # Apliquem el factor de multiplicació
                print("Velocitat: ", valor)
                # REVOLUCIONS DEL MOTOR (rpm)
                valor = tpdo_3.data[5]
                valor = (valor << 8) | tpdo_3.data[4]  # Traiem el valor del missatge
                valor = (valor << 8) | tpdo_3.data[3]  # Traiem el valor del missatge
                valor = (valor << 8) | tpdo_3.data[2]  # Traiem el valor del missatge
                if valor <= 10000:
                    revolucions = valor
                    print("RPM: ",revolucions)
                # VOLTATGE ACCELERADOR (V)
                valor = tpdo_3.data[7]
                valor = (valor << 8) | tpdo_3.data[6]  # Traiem el valor del missatge
                accelerador = valor * 0.0039  # Apliquem el factor de multiplicació
                print("Accelerador: ", accelerador)

            if(message.arbitration_id==0x2F):
                print("Id: ", message.arbitration_id)
                arduino_1.data = message.data
                valor=arduino_1.data
                print("Valor arduino 1: ",valor)




    c+='{0:d},{1:d},{2:d},{3:d},{4:d},{5:d},{6:d},{7:d}'.format(voltatge,corrent,corrent_maxim,temperatura_motor,temperatura_inversor,velocitat,revolucions,accelerador)
    print('\r {} '.format(c))
    print(c,file=outfile)
    count+=1
    
            
            
                
      
                
                
