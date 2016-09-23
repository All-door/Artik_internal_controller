from RedisClient import RedisClient
from Keypad import Keypad
from FaceAuth import FaceAuth
from SettingParser import SettingParser
import os
import time

redisClient = RedisClient()
faceAuth = FaceAuth('Microsoft Face API Key')
keypad = Keypad()
settingParser = SettingParser()

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
        localFaceId = faceAuth.takePicture()
        if localFaceId == 'None':
            keypad.lcdWrite("Face Auth", "try again..")
            print ('Cannot find face')
            continue
        result = faceAuth.compareFaceByIds(remoteFaceId, localFaceId)
        if result == True:
            # Open door
            keypad.lcdWrite("Face Auth", "Welcome!")
            print ('Open Door')
        elif result == False:
            # Not You
            keypad.lcdWrite("Face Auth", "try again..")
            print ('Face Auth Error')
    else:
        remotePassword = redisClient.getPassword()
        if remotePassword == localPassword:
            # Open door
            keypad.lcdWrite("Password Auth", "Welcome!")
            print ('Open Door')
        elif localPassword == settingParser.read()['MASTER_PW']:
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
            keypad.lcdWrite("Password Auth", "Fail! try again")
