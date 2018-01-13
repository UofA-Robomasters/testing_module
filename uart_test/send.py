import sys
import argparse
import serial

# Testing sending message
MSG = [100, 9]

# These are predefined values for the communication protocol:
MSG_START = 0xff
MSG_STOP = 0xfe
MSG_CONFIRM = 0xff
MSG_AXIS = 0xfe

class Communication:
    """
    Comunication class
    """
    
    def __init__(self, port='/dev/ttyTHS2', bitrate=115200):
        self.ser = serial.Serial(port, bitrate, timeout = 0)

    def send(self, data):
        msg = bytearray([data])
        self.ser.write(msg)

    def receive(self):
        msg = self.ser.read(1)
        if len(msg) != 1:
            return None
        else:
            return ord(msg)

    def close(self):
        self.ser.close()

    def send_axis(self, val):
        """
        val: [-128, 127],  which is encoded as [0, 255]
        """
        assert val >= -128 and val <= 127
        self.send([val + 128])


# def parse_user_input():
#     """
#     Parse the command line input argument
#     """
#     description = 'Testing UART3 port on DJI Manifold.'
#     parser = argparse.ArgumentParser(description=description,
#                                      epilog='')
# 
#     requiredNamed = parser.add_argument_group('required arguments')
#     requiredNamed.add_argument('-m','--message',
#                                dest='message',
#                                help='The message sending through UART3 port.',
#                                required=False)
# 
#     args = parser.parse_args(sys.argv[1:])
# 
#     return args



if __name__ == "__main__":
    """
    Main function for testing
    """
    # message
    message = MSG
    
    # parse user input
    # args = parse_user_input()
    
    # print(int(args.message))
    # print(bytearray([255,10,11]))
    # print(0xff)
    uart3 = Communication()
    uart3.send(message)
    uart3.close()