#! /usr/bin/python

# use as a class in another python file.
# when used in standalone mode, choose the /dev/ttyUSB[0-2]
# ./grbl 0  
# ^^^^^^^^ can send one command at a time for verification

import serial, time

class grbl:
    """
    Ed driver try, for the laser engraver
    Make sure your select the correct /dev/ttyUSBx 
    """
    
    def __init__(self, ser="/dev/ttyUSB0", br9600=9600):
        self.SERIALPORT = ser
        #SERIALPORT = "/dev/ttyUSB1"
        self.BAUDRATE = br9600
        self.ser = serial.Serial(self.SERIALPORT, self.BAUDRATE, timeout=0.1)
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE
        self.ser.xonxoff = False
        self.ser.rtscts = False
        self.ser.dsrdtr = False
        self.ser.terminator = "\n"
        # CR=\c LF=\n CR+LF=\c\n
        self.ser.open()
        self.response = ""
        
    def send(self,MESSAGE):
        try:
            self.ser.write(MESSAGE)
            time.sleep(0.2) #<== dont spam it

        except serial.errno as e:
            self.ser.open()
            self.send(MESSAGE)

    def recv(self):
        self.response = ""
        tmp = self.ser.readline().strip('\r\n')
        while tmp:
            self.response += tmp+'\n'
            tmp = self.ser.readline().strip('\r\n')
                #self.response += tmp+'\n'
        return self.response

    def __del__(self):
        self.ser.close()

    def status(self):
        i1=self.send("$$")
        return i1




import sys
import select
import tty
import termios

class NonBlockingConsole(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.readline()
        return False

if __name__ == '__main__':
    nbc = NonBlockingConsole()
    port="0" if len(sys.argv)<=1 else sys.argv[1]
    tty="/dev/ttyUSB"+port
    print "== connecting to "+tty+" and send ^X to reset possible errors =="
    ae =  grbl(tty, 9600)
    print """___exemple:___
             $$
             $? (help)
             F10000 (speed)
             G20 (atfer this units in inches)
             G21 (atfer this units in mm)
             G90 (absolute  position)
             G91 (relative position : incremental)
             G1 X10 Y10
             M03 (start laser)
             M05 (stop laser)
            """
    print '__ To (q)uit, type q__\n'
    msg = chr(24)+'\rG21\rG90' # ^X
    while msg != 'q\n':
        if msg:
           ae.send(msg)
        msg = nbc.get_data()
        ae.recv()
        if ae.response:
            print ae.response

    ae.send("m5\n") #<= turn off laser

