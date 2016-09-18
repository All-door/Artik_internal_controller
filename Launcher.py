from RedisClient import RedisClient
from Keypad import Keypad
from FaceAuth import FaceAuth

redisClient = RedisClient()
faceAuth = FaceAuth('Microsoft Face API Key')
keypad = Keypad()

while True:
    localPassword = keypad.read()
    if localPassword == 'Camera':
        remoteFaceId = redisClient.getFaceId()
        print ('Camera mode')
        if remoteFaceId == 'None':
            #Add Exception
            continue
        localFaceId = faceAuth.takePicture()
        if localFaceId == 'None':
            # Not detect Face
            print ('Cannot find face')
            continue
        result = faceAuth.compareFaceByIds(remoteFaceId, localFaceId)
        if result == True:
            # Open door
            print ('Open Door')
        elif result == False:
            # Not You
            print ('Face Auth Error')
    else:
        remotePassword = redisClient.getPassword()
        if remotePassword == localPassword:
            # Open door
            print ('Open Door')
        else:
            # Not You
            print ('Password Auth Error')
