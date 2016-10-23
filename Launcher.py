from RedisClient import RedisClient
from Keypad import Keypad
from FaceAuth import FaceAuth
from SettingParser import SettingParser
from Buzzer import Buzzer
import os
import time

settingParser = SettingParser()
redisClient = RedisClient()
faceAuth = FaceAuth(settingParser.read()['FACE_API_KEY'])
keypad = Keypad()
buzzer = Buzzer()

while True:
    time.sleep(2)
    keypad.lcdWrite("'*'Camera mode ", "'#'password mode")
    localPassword = keypad.read()
    if localPassword == 'Camera':
        remoteFaceId = redisClient.getFaceId()
        print ('Face mode')
        keypad.lcdWrite("Face Auth", "wait......")
        if remoteFaceId == 'None':
            keypad.lcdWrite("Face Auth", "Not have image")
            continue
        buzzer.beepPicture()
        localFaceId = faceAuth.takePicture()
        buzzer.off()
        if localFaceId == 'None':
            keypad.lcdWrite("Face Auth", "try again..")
            print ('Cannot find face')
            continue
        result = faceAuth.compareFaceByIds(remoteFaceId, localFaceId)
        if result == True:
            # Open door
            keypad.openDoor()
            buzzer.beepOpen()
            time.sleep(1)
            keypad.lcdWrite("Face Auth", "Welcome!")
            print ('Open Door')
        elif result == False:
            # Not You
            buzzer.beepErr()
            keypad.lcdWrite("Face Auth", "try again..")
            print ('Face Auth Error')
    else:
        remotePassword = redisClient.getPassword()
        if remotePassword == localPassword:
            keypad.openDoor()
            time.sleep(1)
            keypad.lcdWrite("Password Auth", "Welcome!")
            print ('Open Door')
            buzzer.beepOpen()
        elif localPassword == settingParser.read()['MASTER_PW']:
            keypad.openDoor()
            time.sleep(1)
            keypad.lcdWrite("Admin", "Welcome")
            print ('Open Door')
        elif localPassword == settingParser.read()['MASTER_PW'] + '*':
            keypad.lcdWrite("Setting Mode", "Wait.....")
            os.system("./softAP/softApTurnOn.sh")
            keypad.lcdWrite("Conn All-Door", "192.168.2.1")
            os.system("python app.py")
            keypad.lcdWrite("Save data", "Wait.....")
            os.system("./softAP/softApTurnOff.sh")
        else:
            # Not You
            print ('Password Auth Error')
            buzzer.beepErr()
            keypad.lcdWrite("Password Auth", "Fail! try again")
