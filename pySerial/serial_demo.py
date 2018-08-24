import sys
import serial

def initUart(com='COM0', baudrate=19200):
#    ser = serial.Serial(
#        port='COM1',            # number of device, numbering starts at
#        baudrate=57600,         # baud rate
#        bytesize=8,             # number of databits
#        parity='None',          # enable parity checking
#        stopbits=1,             # number of stopbits
#        timeout=None,           # set a timeout value, None for waiting forever
#        xonxoff=0,              # enable software flow control
#        rtscts=0,               # enable RTS/CTS flow control
#        interCharTimeout=None   # Inter-character timeout, None to disable
#    )
    ser = serial.Serial()
    ser.port = com
    ser.baudrate=baudrate
    return ser

def main(argv=None):
    mySer = initUart('COM1', 57600)
    print mySer.portstr       # check which port was really used  
    mySer.open()
    mySer.write("hello")      # write a string  
    mySer.close()

if __name__ == "__main__":
    sys.exit(main())

