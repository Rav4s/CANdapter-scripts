# TODO: #1 add file output/logging functionality

import sys
import can
import pyCandapter
import signal
import time
import argparse
from tpee_mppt import mppt_data_readable
from wavesculptor import wavesculptor_data_readable

parser = argparse.ArgumentParser()
# cli flags: -d DEVICE -p PORT -s SERIALBAUDRATE -c CANBAUDRATE -m MPPT_ID -w WS_ID
parser.add_argument("-d", "--device", help="Device (0 MPPT, 1 Moco)")
parser.add_argument("-p", "--port", help="COM Port")
parser.add_argument("-s", "--serial", help="Serial Baud Rate", type=int)
parser.add_argument("-c", "--can", help="CAN Baud Rate", type=int)
parser.add_argument("-m", "--mppt", help="MPPT Base Address")
parser.add_argument("-w", "--moco", help="Moco Base Address")
args = parser.parse_args()

# set vars using flags
device = args.device
port = args.port
serialbaudrate = args.serial
canbaudrate = args.can
mppt_id = args.mppt
ws_id = args.moco

# if flags unset, set default COM port, baud rate, and CAN bus speed (currently 125k for Daybreak)
port = "COM4" if port is None else port
serialbaudrate = 9600 if serialbaudrate is None else serialbaudrate
canbaudrate = 125000 if canbaudrate is None else canbaudrate
DEFAULT_MPPT_ID = "0x200"
DEFAULT_WS_ID = "0x240"

# close CAN bus before terminating
def signal_handler(sig, frame):
    candapter.closeCANBus()
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

'''
# create candapter instance
try:
    candapter = pyCandapter.pyCandapter(port, serialbaudrate)
    candapter.openCANBus(canbaudrate)    
except Exception as e:
    print("Failed to open CAN Bus. Exiting...")
    print(f"Full Error: {e}")
    candapter.closeCANBus()
    exit(1)
'''

print("CANdapter Scripts for the TPEE SEC-B175-7A MPPT and Prohelion Wavesculptor 22 Motor Controller")
device = input("Enter 0 for MPPT or 1 for Motor Controller: ") if device is None else device

if device == "0":
    mppt_id = input("Enter the MPPT Device ID (Press enter for default): ") if mppt_id is None else mppt_id
    if mppt_id == "":
        mppt_id = DEFAULT_MPPT_ID
    mppt_id_int = int(mppt_id, 16) # convert to int cause python is ew
    print(f"\n\n\nCAN frames for MPPT at {mppt_id}:")
    # loop to read CAN messages
    while True:

          
        # messages to test if translation is working (remove for prod)
        message = can.Message(arbitration_id=0x200, data=[0x02, 0xB7, 0xFF, 0x8D, 0x0C, 0x8C, 0xFF, 0xCD], is_extended_id=False)
        #test_message = can.Message(arbitration_id=0x201, data=[0x02, 0x00, 0x00, 0x17, 0x17], is_extended_id=False)
        
        #message = candapter.readCANMessage()
        if message is not None:
            print(mppt_data_readable(mppt_id_int, message))
        
        time.sleep(0.05) # oversampling so candapter FIFO doesn't fill up (do we even need a delay????)
        
elif device == "1":
    ws_id = input("Enter the Motor Controller Device ID (Press enter for default): ") if ws_id is None else ws_id
    if ws_id == "":
        ws_id = DEFAULT_WS_ID
    ws_id_int = int(ws_id, 16) # convert to int cause python is ew
    print(f"\n\n\nCAN frames for Motor Controller at {ws_id}:")
    # loop to read CAN messages
    while True:
        
        # messages to test if translation is working (remove for prod)
        test_message = can.Message(arbitration_id=0x200, data=[0x02, 0xB7, 0xFF, 0x8D, 0x0C, 0x8C, 0xFF, 0xCD], is_extended_id=False)
        #test_message = can.Message(arbitration_id=0x201, data=[0x02, 0x00, 0x00, 0x17, 0x17], is_extended_id=False)
        message = wavesculptor_data_readable(ws_id_int, test_message)
        
        #message = candapter.readCANMessage()
        if message is not None:
            print(message)
        time.sleep(0.05) # oversampling so candapter FIFO doesn't fill up (do we even need a delay????)
else:
    print("Invalid input. Exiting...")
    candapter.closeCANBus()
    exit(1)