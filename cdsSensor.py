import sys
import time

class CdsSensor:

    def __init__(self, pinNum):
        self.pinNum = pinNum

    def setup(self):
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum
        pinctldir = open(filename, "rb", 0)
        pinctldir.close()

    def RCtime(self):
        self.setup()
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum
        pin = open(filename, "rb", 0)
        readPin = pin.read()
        voltage = int(readPin)*(5/4095)
        lux = (voltage-0.022)*100/(0.666)

        return round(lux,4)

if __name__=="__main__":
    sensor = CdsSensor(0)
    print("Lux :",sensor.RCtime())