import cognitive_face as CF
import json

class FaceAuth:
    def __init__(self, key):
        CF.Key.set(key);

    def getFaceId(self, url):
        return CF.face.detect(url)[0]['faceId']

    def compareFaceByIds(self, faceId1, faceId2):
        return CF.face.verify(faceId1, faceId2, None, None)['isIdentical']

    def compareFaceByImgs(self, url1, url2):
        return self.compareFaceByIds(self.getFaceId(url1), self.getFaceId(url2))

if __name__ == "__main__":
    KEY = 'Microsoft FaceAPI Key'
    face = FaceAuth(KEY)

    print (face.compareFaceByImgs('./123.jpg', './456.jpg'))
