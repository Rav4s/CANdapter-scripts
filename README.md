# CANdapter-scripts
Scripts to convert input from a [CANdapter](https://www.ewertenergy.com/products.php?item=candapter) (CAN bus to USB interface) to human-readable output. Supports CAN message decoding for the [TPEE SEC-B175-7A MPPT](https://www.tpee.nl/product/sec-b175-7a/) and the [Prohelion Wavesculptor 22 Motor Controller](https://prohelion.com/shop/wavesculptor-motor-controllers/wavesculptor22-motor-controller/) (WIP) used on the 2025 Longhorn Racing Solar car.

## Install
Run ```pip3 install -r requirements.txt``` in your virtual environment to install the necessary dependencies.

## Usage
Run ```py main.py``` and follow the prompts to select your device type and base address. To change the COM port, serial baud rate, or CAN baud rate, set the ```PORT```, ```SERIALBAUDRATE```, and ```CANBAUDRATE``` configuration variables. Alternatively, use the command line flags as outlined below for one-line execution:  
```
-d DEVICE (0 for MPPT, 1 for Motor Controller)
-p PORT (CANdapter COM Port)
-s SERIAL (Serial Baud Rate)
-c CAN (CAN Baud Rate)
-m MPPT (MPPT Base Address)
```

## Acknowledgement
pyCandapter.py is from https://github.com/Anay1440/pyCandapter developed by Anay Patil, used under the MIT License (thx goat).