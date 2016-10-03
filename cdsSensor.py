import sys

class CdsSensor:

    def __init__(self, pinNum):
        self.pinNum = pinNum

    def getBright(self):
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum
        pin = open(filename, "rb", 0)
        readPin = pin.read()
        voltage = int(readPin)*(5/4095)
        lux = (voltage-0.022)*100/(0.666)
        pin.close()
        return round(lux,4)

if __name__=="__main__":
    sensor = CdsSensor(0)
    print("Lux :",sensor.getBright())