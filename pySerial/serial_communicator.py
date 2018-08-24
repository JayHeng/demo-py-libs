
#key notes:
# 1. Standard program structure - __main__
# 2. Basic usage of "serial" package
# 3. Concept of global variable - global
# 4. Concept of sub-function - def
# 5. I/O interaction on console
#    5.1 raw_input() - real-time echo
#    5.2 sys.stdin.read() - real-time echo
#    5.3 getpass.getpass() - no echo
#    5.4 print - add '\n' to the end
#    5.5 sys.stdout.write() - no '\n' to the end
# 6. Timing trigger thread- threading.Timer()
#    6.1 thread task is only executed once
#    6.2 install task by itself to make it periodic task

import sys
import serial
import threading
import getpass

s_task_interval = 0.5

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

def uart_sent(ser,string):
    if not ser.isOpen():
        ser.open()
    ser.write(string)

def uart_receive(ser,num):
    if not ser.isOpen():
        ser.open()
    string = ser.read(num)
    return string

def periodic_receive_task(ser, interval):
    num = ser.inWaiting()
    if num != 0:
        recvString = uart_receive(ser,num)
        sys.stdout.write("\n" + ser.port + '->: ' + recvString)
    threading.Timer(interval, periodic_receive_task, (ser, interval)).start()

def blocking_send_task(ser):
    #sentString = raw_input("sent: ")
    #sentString += '\n'
    sentString = getpass.getpass(prompt='')
    sys.stdout.write(ser.port + '<-: ' + sentString)
    uart_sent(ser, sentString)

def main(argv=None):
    mySer = initUart(sys.argv[1],sys.argv[2])
    #    print mySer.portstr       # check which port was really used
    mySer.open()
    global s_task_interval
    periodic_receive_task(mySer, s_task_interval)
    while True:
        blocking_send_task(mySer)

if __name__ == "__main__":
    sys.exit(main())
