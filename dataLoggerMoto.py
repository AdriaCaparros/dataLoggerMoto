mport can
import time
import os


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

speed=0
voltage=0
temp1=0
c=''
count=0


while True:
    for j in range(3):
        message = bus.recv(timeout=1.0)
        if message is not None:
            s=0
            for i in range(message.dlc):
                s|=message.data[i]<<(8*i)
                
            c='{0:f},{1:d},'.format(message.timestamp,count)
            if (message.arbitration_id == 0x274):
                print("Data: ",s)
                print("Id: ", message.arbitration_id)
                tpdo_1.data = message.data
                
            if (message.arbitration_id == 0x195):
                print("Data: ",s)
                print("Id: ", message.arbitration_id)
                tpdo_2.data = message.data
                
            if (message.arbitration_id == 0x146):
                print("Data: ",s)
                print("Id: ", message.arbitration_id)
                tpdo_3.data = message.data
        
    
    c+='{0:d},{1:d},{2:d}'.format(0,0,0)
    print('\r {} '.fromat(c))
    print(c,file=outfile)
    count+=1
    
            
            
                
      
                
                
