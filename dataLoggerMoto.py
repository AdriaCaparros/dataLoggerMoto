import can
import time
import os
import queue
from threading import Thread

VEHICLE_SPEED = 0xA0

outfile=open('log.txt','w')

print('\n\rCAN Rx test')
print('Bring up CAN0...')

#Bring up can0 interface at 500kbps

os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Ready')

try:
    bus = can.interface.Bus(channel='can0',bustype='socketcan_native')
    
except OSError:
    print('Cannot find PiCan board.')
    exit()

def can_rx_task():
    while True:
        message = bus.recv()
        q.put(message)
    
 
q=queue.Queue()
rx= Thread(target=can_rx_task)
rx.start()

speed=0
count=0
c=''

try:
    while True:
        for i in range(1):
            while(q.empty()==True):
                pass
            message = q.get()
            for j in range(message.dlc):
                s |=message.data[j]<<(8*j)
            
            c='{0:f},{1:d},'.format(message.timestamp,count)
            if message.aritration_id==0xA0:
                speed=s
        
        c+='{0,d}'.format(speed)
        print('\r{}'.format(c))
        print(c,file=outfile)
        count+=1

except KeyboardInterrupt:
    outfile.close()
    os.system("sudo /sbin/ip link set can0 down")
    print('\n\rKeyboard interrupt')
    
                
    
        
                
                
                
                
                
