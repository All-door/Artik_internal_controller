import sys
import time
import math

class MqSensor:

    def __init__(self, pinNum):
        self.pinNum = pinNum

    def getResisCacul(self, raw_adc):
        return 5*(4095-raw_adc)/raw_adc

    def calibration(self):
        val=0
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum
        for i in range(0,50):
            time.sleep(0.5)
            pin = open(filename, "rb",0)
            val+=self.getResisCacul(int(pin.read()))
            pin.close()

        val= val/(50*9.83)
        return val

    def mqRead(self):
        rs = 0
        filename = '/sys/devices/12d10000.adc/iio:device0/in_voltage%d_raw' % self.pinNum

        for i in range(0, 50):
            pin = open(filename, "rb", 0)
            rs+=self.getResisCacul(int(pin.read()))
            time.sleep(0.05)
            pin.close()
        rs= rs/50

        return rs

    def getPercent(self, ratio, gas):
        return math.pow(10, (((math.log10(ratio)-gas[1])/gas[2])+gas[0]))

    def getGasPercent(self, ratio, gas_id):
        lpg = [2.3, 0.21, -0.47]
        co = [2.3, 0.72, -0.34]
        smoke = [2.3, 0.53, -0.44]
        if gas_id ==0:
            return self.getPercent(ratio, lpg)
        if gas_id ==1:
            return self.getPercent(ratio, co)
        if gas_id ==2:
            return self.getPercent(ratio, smoke)

    def getLpgCoSmoke(self):
        ro = self.calibration()
        lpg = self.getGasPercent(self.mqRead()/ro, 0)
        co = self.getGasPercent(self.mqRead()/ro, 1)
        smoke = self.getGasPercent(self.mqRead()/ro, 2)

        return lpg, co, smoke

if __name__=="__main__":
    sensor = MqSensor(2)
    print(sensor.getLpgCoSmoke())
