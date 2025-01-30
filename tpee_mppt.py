import can

# convert raw CAN frames from MPPT to human readable data
# reference: https://www.tpee.nl/wp-content/uploads/2024/10/OpenSEC-firmware-Manual.pdf
def mppt_data_readable(devID, message) -> list[str]:

    # figure out how to identify which message being sent, and then call diff function for each one?
    
    result = "Hello"

    return result