# TODO: #1 add file output/logging functionality

import sys
import can
import pyCandapter
import signal
import time
from tpee_mppt import mppt_data_readable
from wavesculptor import wavesculptor_data_readable

# change to CANdapter COM port, baud rate, and CAN bus speed (currently 125k for Daybreak)
PORT = 'COM4'
SERIALBAUDRATE = 9600
CANBAUDRATE = 250000

DEFAULT_MPPT_ID = "0x200"

# create candapter instance
candapter = pyCandapter.pyCandapter(PORT, SERIALBAUDRATE)
candapter.openCANBus(CANBAUDRATE)

# close CAN bus before terminating
def signal_handler(sig, frame):
    candapter.closeCANBus()
    exit(0) 

signal.signal(signal.SIGINT, signal_handler)

print("CANdapter Scripts for the TPEE SEC-B175-7A MPPT and Prohelion Wavesculptor 22 Motor Controller")
device = input("Enter 0 for MPPT or 1 for Motor Controller: ")

if device == "0":
    mppt_id = input("Enter the MPPT Device ID (Press enter for default): ")
    if mppt_id == "":
        mppt_id = DEFAULT_MPPT_ID
    mppt_id_int = int(mppt_id, 16) # convert to int cause python is ew
    print(f"\n\n\nCAN frames for MPPT at {mppt_id}:")
    # loop to read CAN messages
    while True:
        # print(chr(27) + "[2J") # clear the console (maybe better to not have this?)
        message = candapter.readCANMessage()
        if message is not None:
            print(mppt_data_readable(mppt_id, message))
            
        # messages to test if translation is working (remove for prod)
        '''test_message = can.Message(arbitration_id=0x200, data=[0x02, 0xB7, 0xFF, 0x8D, 0x0C, 0x8C, 0xFF, 0xCD], is_extended_id=False)
        test_message = can.Message(arbitration_id=0x201, data=[0x02, 0x00, 0x00, 0x17, 0x17], is_extended_id=False)
        test_string = mppt_data_readable(mppt_id_int, test_message)
        print(test_string)'''
        time.sleep(0.5)
        
elif device == "1":
    print("CAN frames for Motor Controller:")
    # loop to read CAN messages
    while True:
        message = candapter.readCANMessage()
        if message is not None:
            print(message)
else:
    print("Invalid input. Exiting...")
    exit(1)