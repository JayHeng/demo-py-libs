import sys
import serial
import threading
import time

s_task_interval = 1

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

def periodic_bridge_task(recvSer, sendSer, interval):
    num = recvSer.inWaiting()
    if num != 0:
        recvString = uart_receive(recvSer, num)
        uart_sent(sendSer, recvString)
    threading.Timer(interval, periodic_bridge_task, (recvSer, sendSer, interval)).start()

def main(argv=None):
    com = [sys.argv[1], sys.argv[2]]
    baud = sys.argv[3]
    mySerA = initUart(com[0], baud)
    mySerB = initUart(com[1], baud)
    mySerA.open()
    mySerB.open()
    global s_task_interval
    periodic_bridge_task(mySerA, mySerB, s_task_interval)
    time.sleep(s_task_interval / 2)
    periodic_bridge_task(mySerB, mySerA, s_task_interval)
    while True:
        pass

if __name__ == "__main__":
    sys.exit(main())
