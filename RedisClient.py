import redis

class RedisClient:
    def __init__(self):
        self.redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
    def getPassword(self):
        return self.redisClient.get('Password').decode('utf-8')
    def getFaceId(self):
        return self.redisClient.get('FaceId').decode('utf-8')
    def getArtikDeviceId(self):
        return self.redisClient.get('ArtikDeviceId').decode('utf-8')


if __name__=='__main__':
    redisClient = RedisClient()
    print (redisClient.getPassword())

