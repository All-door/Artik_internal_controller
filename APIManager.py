import json
import http.client
import redis
import time

class APIManager(object):
    """All-Door for Artik API 통신관련 라이브러리"""
    def __init__(self, apiUrl='localhost:3000', redisUrl='localhost', redisPort=6379, deviceId='1',tickSecond=5):
        print('API Manager Init...')
        super(APIManager, self).__init__()
        self.apiUrl = apiUrl
        self.redisUrl = redisUrl
        self.redisPort = redisPort
        self.deviceId = deviceId
        self.tickSecond = tickSecond
        self.stop = False
        self.headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            }
        self.printArgument()
        self.initRedis()

    def printArgument(self):
        print('API URL :', self.apiUrl)
        print('Redis URL :', self.redisUrl)
        print('Reids PORT:', self.redisPort)
        print('Device ID :', self.deviceId)
        print('Tick Second :', self.tickSecond,'s')

    def initRedis(self):
        self.redis = redis.StrictRedis(host=self.redisUrl, port=self.redisPort, db=0)

    def routine(self):
        while True:
            try:
                conn = http.client.HTTPConnection(self.apiUrl)
                conn.request("POST", "/api/device/" + self.deviceId, "", self.headers)
                data = conn.getresponse().read()
                data_json = json.loads(data.decode("utf-8"))

                print('Password :', data_json['pw1'])
                print('FaceId :', data_json['FaceId'])
                print('Artik Cloud Device Id :', data_json['ArtikDeviceID'])
                print('Artik Cloud Device Access Token :', data_json['ArtikDeviceAccessToken'])

                self.redis.set('Password', data_json["pw1"])
                self.redis.set('FaceId', data_json['FaceId'])
                self.redis.set('ArtikDeviceId', data_json['ArtikDeviceID'])
                self.redis.set('ArtikDeviceAccessToekn', data_json['ArtikDeviceAccessToken'])
            except Exception as e:
                print(e)
            time.sleep(self.tickSecond)

if __name__ == '__main__':
    APIManager().routine()
