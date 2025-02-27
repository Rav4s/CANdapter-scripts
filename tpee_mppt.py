import can
import cantools

DEFAULT_MPPT_ID = 0x200
mpptdb = cantools.database.load_file('files/tpee_mppt.dbc')

# convert unsigned to signed 16-bit int
def convert_to_signed(unsigned):
    if unsigned <= 32767:
        return unsigned
    else:
        return unsigned - 65536

# convert raw CAN frames from MPPT to human readable data
# reference: https://www.tpee.nl/wp-content/uploads/2024/10/OpenSEC-firmware-Manual.pdf
def mppt_data_readable(devID, message) -> str:
    # dynamically update message id to match base+offset as defined in dbc file
    updated_id = message.arbitration_id - (devID - DEFAULT_MPPT_ID)
    try:
        decoded_message = mpptdb.decode_message(updated_id, message.data) # decode message using dbc
        print(decoded_message)
    except:
        print("Failed to decode message!")

# convert raw CAN frames from MPPT to human readable data
# reference: https://www.tpee.nl/wp-content/uploads/2024/10/OpenSEC-firmware-Manual.pdf
def mppt_data_readable1(devID, message) -> str:    
    message_data = message.data
    packet_ID = message.arbitration_id - devID
    
    # TODO: proper error handling for malformed CAN messages
    
    # packet IDs as defined in datasheet
    match packet_ID:
        case 0:            
            # power measurements
            input_voltage = 0.01 * float(convert_to_signed((message_data[0] << 8) | message_data[1])) # bytes 0-1
            input_current = 0.0005 * float(convert_to_signed((message_data[2] << 8) | message_data[3])) # bytes 2-3
            output_voltage = 0.01 * float(convert_to_signed((message_data[4] << 8) | message_data[5])) # bytes 4-5
            output_current = 0.0005 * float(convert_to_signed((message_data[6] << 8) | message_data[7])) # bytes 6-7
            
            output_string = "Input Voltage: " + str(round(input_voltage, 3)) + "V    Input Current: " + str(round(input_current, 3)) + "A     Output Voltage: " + str(round(output_voltage, 3)) + "V     Output Current: " + str(round(output_current, 3)) + "A"
            return output_string
        case 1:
            # status
            match message_data[0]:
                case 0:
                    mode = "Constant Input Voltage"
                case 1:
                    mode = "Constant Input Current"
                case 2:
                    mode = "Minimum Input Current"
                case 3:
                    mode = "Constant Output Voltage"
                case 4:
                    mode = "Constant Output Current"
                case 5:
                    mode = "Temperature De-rating"
                case 6:
                    mode = "Fault"
                case _:
                    mode = "Invalid"
                    
            match message_data[1]:
                case 0:
                    fault = "OK (No Error)"
                case 1:
                    fault = "Configuration Error"
                case 2:
                    fault = "Input Over Voltage"
                case 3:
                    fault = "Output Over Voltage"
                case 4:
                    fault = "Output Over Current"
                case 5:
                    fault = "Input Over Current"
                case 6:
                    fault = "Input Under Current"
                case 7:
                    fault = "Phase Over Current"
                case 8:
                    fault = "Fault"
                case _:
                    fault = "Invalid"
                    
            match message_data[2]:
                case 0:
                    is_enabled = "Boost Disabled"
                case 1:
                    is_enabled = "Boost Enabled"
                case _:
                    is_enabled = "Invalid"
                    
            ambient_temp = message_data[3]
            heatsink_temp = message_data[4]
            
            output_string = "Mode: " + mode + "     Fault: " + fault + "    Enable: " + is_enabled + "    Ambient: " + str(ambient_temp) + "C     Heatsink: " + str(heatsink_temp) + "C"
                
            return output_string
        case _:
            return "Invalid packet ID"