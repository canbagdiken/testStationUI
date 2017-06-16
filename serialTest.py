from serial.tools import list_ports
import serial
import time

waitingTime = 0.1
connectionTimeOut = 3000

def waitResponse():
    cmd = ""
    x=0
    while(cmd == ""):
        if((x*waitingTime)>connectionTimeOut):
            break
        x = x+1
        cmd = ser.read(ser.inWaiting()).replace("\n","").replace("\r","")
        time.sleep(waitingTime)
    return cmd

def waitCommand(wantedCMD):
    while(waitResponse() != wantedCMD):
        return False
    return True


ser = serial.Serial("/dev/cu.usbmodem1461")
print("Connecting...")
ser.write(b's')
## wait for welcome msg
if(waitCommand("WELCOME")):
    print("welcome msg has been get")

## check double
ser.write(b'REURDY')

if(waitCommand("YES")):
    print("that is ready")
else:
    print("no that is not ready.")


## check double
ser.write(b'IGNPRCDR')
print("IGNITON!!!")







print("I get data.")

ser.close()

"""
### list serials
try:
    for port in list_ports.comports():
        try:
            portAdd = port[0]
            ser = serial.Serial(portAdd)
            print(ser)
            line = ser.readline()
            ser.close()
        except (OSError, serial.SerialException):
            pass


    #cdc = next(list_ports.grep("MyCDCDevice"))
    # Do connection stuff on cdc
except StopIteration:
    print "No device found"
"""
