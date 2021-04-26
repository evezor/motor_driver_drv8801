# DVR8801 Driver Board 

from machine import Pin
from pyb import CAN, Timer
import utime

print("starting Low Power Mosfet test")
print("v1.0")
print("initializing")
can = CAN(1, CAN.NORMAL)
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))

#Setup Pins
HBT_LED = Pin("D13", Pin.OUT)
FUNC_BUTTON = Pin("D5", Pin.IN, Pin.PULL_UP) 
NEO_STATUS = Pin("D8", Pin.OUT)
can_wakeup = Pin("D6", Pin.OUT)
can_wakeup.value(0)



# Set up motor B

b_enable = Pin("A5", Pin.OUT)
b_decay_mode = Pin("A2", Pin.OUT)  # this is the decay mode of the driver. High for slow decay mode
b_decay_mode.value(1)

a_brake = Pin("A3", Pin.OUT)  # motor brake.  Driver must be in slow decay mode for brake to have effect  
b_direction = Pin("A4", Pin.OUT)

b_fault = Pin("E0", Pin.IN, Pin.PULL_UP)
b_sleep = Pin("E1", Pin.OUT)
b_sleep.value(1) #wake the driver up




    #Setup hbt timer
hbt_state = 0
hbt_interval = 500
start = utime.ticks_ms()
next_hbt = utime.ticks_add(start, hbt_interval)
HBT_LED.value(hbt_state)


print("starting")


def chk_hbt():
    global next_hbt
    global hbt_state
    now = utime.ticks_ms()
    if utime.ticks_diff(next_hbt, now) <= 0:
        if hbt_state == 1:
            hbt_state = 0
            HBT_LED.value(hbt_state)
            #print("hbt")
        else:
            hbt_state = 1
            HBT_LED.value(hbt_state)  
        
        next_hbt = utime.ticks_add(next_hbt, hbt_interval)

      

def send():
    can.send('drv8801', 123)   # send a message with id 123
    
def get():
    mess = can.recv(0)
    print(mess)
    simple_test()
    

def simple_test():
    print("test started")
    a_enable.value(1)
    utime.sleep_ms(1000)
    a_enable.value(0)
    a_direction(1)
    a_enable.value(1)
    utime.sleep_ms(1000)
    a_enable.value(0)
    a_direction(0)
    print("test_done")

    
while True:
    chk_hbt()
    if not (FUNC_BUTTON.value()):
        print("function button")
        #send()
        simple_test()
        utime.sleep_ms(200)
    
    if not (b_fault.value()):
        print("Motor B has a Fault!!")
        utime.sleep_ms(200)
    
    if(can.any(0)):
        get()
