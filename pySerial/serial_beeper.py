import sys
import serial
import threading
import getpass
import time

s_task_interval = 1
s_last_ser = None

def initUart(com='COM0', baudrate=19200):
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

def periodic_beeper_task(ser, interval):
    num = ser.inWaiting()
    if num != 0:
        recvString = uart_receive(ser, num)
        sys.stdout.write("\n" + ser.port + '->: ' + recvString)
        global s_last_ser
        s_last_ser = ser
    threading.Timer(interval, periodic_beeper_task, (ser, interval)).start()

def blocking_send_task():
    sentString = getpass.getpass(prompt='')
    global s_last_ser
    ser = s_last_ser
    sys.stdout.write(ser.port + '<-: ' + sentString)
    uart_sent(ser, sentString)

def main(argv=None):
    com = [sys.argv[1], sys.argv[2]]
    baud = sys.argv[3]
    mySerA = initUart(com[0], baud)
    mySerB = initUart(com[1], baud)
    mySerA.open()
    mySerB.open()
    global s_task_interval
    periodic_beeper_task(mySerA, s_task_interval)
    time.sleep(s_task_interval / 3)
    periodic_beeper_task(mySerB, s_task_interval)
    while True:
        blocking_send_task()

if __name__ == "__main__":
    sys.exit(main())
