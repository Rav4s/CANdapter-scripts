import can
import cantools

wavesculptordb = cantools.database.load_file('files/wavesculptor.dbc')

# convert raw CAN frames from motor controller to human readable data
def wavesculptor_data_readable(devID, message) -> str:
    result = "Hello"
    
    # need to implement this

    return result