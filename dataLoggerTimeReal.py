import time
import os
import can
import math
import RPi.GPIO as GPIO


os.remove("/media/pi/AFEC-4877/tpdo1.csv")
os.remove("/media/pi/AFEC-4877/tpdo2.csv")
os.remove("/media/pi/AFEC-4877/tpdo3.csv")
os.remove("/media/pi/AFEC-4877/arduino1.csv")

outfile_tpdo1=open('/media/pi/AFEC-4877/tpdo1.csv','w')
outfile_tpdo2=open('/media/pi/AFEC-4877/tpdo2.csv','w')
outfile_tpdo3=open('/media/pi/AFEC-4877/tpdo3.csv','w')
outfile_arduino1=open('/media/pi/AFEC-4877/arduino1.csv','w')


print('\n\rCAN Rx test')
print('Bring up CAN0...')

#Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 down")
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Ready')
bus = can.interface.Bus(channel='can0',bustype='socketcan_native')

tpdo_1= can.Message(data=[0,0,0,0,0,0,0,0],arbitration_id=0x274)
tpdo_2= can.Message(data=[0,0,0,0,0,0,0,0],arbitration_id=0x195)
tpdo_3= can.Message(data=[0,0,0,0,0,0,0,0],arbitration_id=0x146)
arduino_1 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x2F)
arduino_2 = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], arbitration_id=0x3F)

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)
switch_state=False




voltatge=0
corrent=0
corrent_maxim=0
temperatura_motor=0
temperatura_inversor=0
velocitat=0
revolucions=0
accelerador=0
temperatura1=0
temperatura2=0
temperatura3=0
temperatura4=0
c=''
count=0
valor=0



while (switch_state==False):
    switch_state=GPIO.input(24)
while (switch_state==True):
    message = bus.recv(timeout=1.0)
    if message is not None:
        valor=0
        c = '{0:f},{1:d},'.format(message.timestamp, count)
        if (message.arbitration_id==0x274):
            print("Id: ",message.arbitration_id)
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
            print("Corrent maxim: ", corrent_maxim)
            c += '{0:f},{1:f},{2:f}'.format(voltatge, corrent, corrent_maxim)
            print('\r {} '.format(c))
            print(c, file=outfile_tpdo1)  # Save data to file
            count += 1
        if (message.arbitration_id == 0x195):
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
            c += '{0:f},{1:f}'.format(temperatura_motor, temperatura_inversor)
            print('\r {} '.format(c))
            print(c, file=outfile_tpdo2)  # Save data to file
            count += 1
        if (message.arbitration_id == 0x146):
            print("Id: ", message.arbitration_id)
            tpdo_3.data = message.data
            valor = tpdo_3.data[1]
            valor = (valor << 8) | tpdo_3.data[0]  # Traiem el valor del missatge
            valor = valor * 0.0625  # Apliquem el factor de multiplicació
            if valor <= 240:  # Si es un valor invalid, no el guardem
                velocitat = valor
                print("Velocitat: ", velocitat)
            # REVOLUCIONS DEL MOTOR (rpm)
            valor = tpdo_3.data[5]
            valor = (valor << 8) | tpdo_3.data[4]  # Traiem el valor del missatge
            valor = (valor << 8) | tpdo_3.data[3]  # Traiem el valor del missatge
            valor = (valor << 8) | tpdo_3.data[2]  # Traiem el valor del missatge
            if valor <= 10000:
                revolucions = valor
                print("RPM: ", revolucions)
            # VOLTATGE ACCELERADOR (V)
            valor = tpdo_3.data[7]
            valor = (valor << 8) | tpdo_3.data[6]  # Traiem el valor del missatge
            accelerador = valor * 0.0039  # Apliquem el factor de multiplicació
            print("Acceleracio: ", accelerador)
            c += '{0:f},{1:f},{2:f}'.format(velocitat, revolucions, accelerador)
            print('\r {} '.format(c))
            print(c, file=outfile_tpdo3)  # Save data to file
            count += 1
        if (message.arbitration_id==0x2F):
            print("Id: ", message.arbitration_id)
            arduino_1.data = message.data
            valor = arduino_1.data
            valor = arduino_1.data[1]
            valor = (valor << 8) | arduino_1.data[0]
            valor = valor * 0.01
            if valor != 0:
                temperatura1 = valor
                print('Temp1 (Graus Centigrads): ', temperatura1)

            valor = arduino_1.data[3]
            valor = (valor << 8) | arduino_1.data[2]
            valor = valor * 0.01
            if valor != 0:
                temperatura2 = valor
                print('Temp2 (Graus Centigrads): ', temperatura2)
            valor = arduino_1.data[5]
            valor = (valor << 8) | arduino_1.data[4]
            valor = valor * 0.01
            if valor != 0:
                temperatura3 = valor
                print('Temp3 (Graus Centigrads): ', temperatura3)
            valor = arduino_1.data[7]
            valor = (valor << 8) | arduino_1.data[6]
            valor = valor * 0.01
            if valor != 0:
                temperatura4 = valor
                print('Temp4 (Graus Centigrads): ', temperatura4)
            c += '{0:f},{1:f},{2:f},{3:f}'.format(temperatura1,temperatura2,temperatura3,temperatura4)
            print('\r {} '.format(c))
            print(c, file=outfile_arduino1)  # Save data to file
            count += 1
        switch_state = GPIO.input(24)



outfile_tpdo1.close()     # Close logger file
outfile_tpdo2.close()
outfile_tpdo3.close()
outfile_arduino1.close()
os.system("sudo /sbin/ip link set can0 down")
print('\n\rData Logger interrupt')
