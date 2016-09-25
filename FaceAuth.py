import cognitive_face as CF
import json
import os

class FaceAuth:
    def __init__(self, key):
        CF.Key.set(key);

    def takePicture(self):
        os.system('fswebcam  -i 0 -d v4l2:/dev/video0  --jpeg 95 --save alldoor.jpg -r 640x480 -S 30')
        try:
            id = self.getFaceId('./alldoor.jpg')
            os.system('rm -f ./alldoor.jpg')
        except:
            return 'None'
        return id

    def getFaceId(self, url):
        return CF.face.detect(url)[0]['faceId']

    def compareFaceByIds(self, faceId1, faceId2):
        return CF.face.verify(faceId1, faceId2, None, None)['isIdentical']

    def compareFaceByImgs(self, url1, url2):
        return self.compareFaceByIds(self.getFaceId(url1), self.getFaceId(url2))

if __name__ == "__main__":
    KEY = 'Microsoft Face Api Key'
    face = FaceAuth(KEY)

    print (face.takePicture())
    print (face.compareFaceByImgs('./123.jpg', './456.jpg'))
