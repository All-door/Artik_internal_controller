import os
import serial

class Keypad:
    dev = '/dev/ttyACM0'
    #dev = 'dev/ttyACM1'
    baud = 9600
    def __init__(self):
        self.serial = serial.Serial(self.dev, self.baud)
        self.serial.flush()

    def lcdWrite(self, firstString, secondString):
        sendMsg = firstString + ':' + secondString + '\n'
        self.serial.write(sendMsg.encode())

    def read(self):
        while True:
            ch = self.serial.read().decode("utf-8")
            if ch == '*':
                return 'Camera'
            if ch == '#':
                self.lcdWrite("PASSWORD", " ")
                pwChar = "";
                pw = list();
                while True:
                    ch = self.serial.read().decode("utf-8")
                    print (ch)
                    pwChar = pwChar + '*'
                    self.lcdWrite("PASSWORD", pwChar)
                    if ch == '#':
                        return ''.join(pw)
                    pw.append(ch)


if __name__ == '__main__':
    keypad = Keypad()
    print(keypad.read())
