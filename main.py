import pyCandapter
import can
import signal
import tpee_mppt
import wavesculptor

# change to CANdapter COM port, baud rate, and CAN bus speed (currently 125k for Daybreak)
PORT = 'COM4'
SERIALBAUDRATE = 9600
CANBAUDRATE = 125000

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

# loop to read CAN messages
while True:
    message = candapter.readCANMessage()
    if message is not None:
        print(message)