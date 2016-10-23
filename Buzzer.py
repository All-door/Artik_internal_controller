import os
import time

class Buzzer:

    def __init__(self):
        self.pwm0_path = "/sys/class/pwm/pwmchip0/"
        os.system("echo 0 > " + self.pwm0_path + "export")
        os.system("echo 1000000 > " + self.pwm0_path + "pwm0/period")

    def settingPeriod(self, period):
        os.system("echo " +  period + "  > " + self.pwm0_path + "pwm0/period")

    def settingDutyCycle(self, cycle):
        os.system("echo " +  cycle + "  > " + self.pwm0_path + "pwm0/duty_cycle")

    def enablePwm(self, msg):
        if msg == True:
            os.system("echo 1 > " + self.pwm0_path + "pwm0/enable")
        else:
            os.system("echo 0 > " + self.pwm0_path + "pwm0/enable")

    def on(self):
        self.enablePwm(True)

    def off(self):
        self.enablePwm(False)

    def beep(self):
        self.settingDutyCycle("500000")
        self.settingPeriod("1000000")
        self.on()
        time.sleep(0.15)
        self.off()

    def beepOpen(self):
        self.settingDutyCycle("0")
        self.settingPeriod("1000000")
        self.on()
        self.settingDutyCycle("400000")
        time.sleep(0.1)
        self.settingDutyCycle("500000")
        time.sleep(0.1)
        self.settingDutyCycle("600000")
        time.sleep(0.1)
        self.off()

    def beepErr(self):
        self.settingPeriod("10000000")
        self.settingDutyCycle("5000000")
        self.on()
        time.sleep(0.5)
        self.off()

    def beepPicture(self):
        self.settingPeriod("100000000")
        self.settingDutyCycle("50000000")
        self.on()

if __name__=="__main__":
    buzzer = Buzzer()
    buzzer.beepPicture()
    time.sleep(3)
    buzzer.off()
