import sys

class HallSensor:

    def __init__(self, pinNum):
        self.pinNum = pinNum

    def getOpened(self):
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum
        pin = open(filename, "rb", 0)

        return int(pin.read())

if __name__=="__main__":
    sensor = HallSensor(1)
    print(sensor.getOpened())
