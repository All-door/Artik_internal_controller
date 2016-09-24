from random import randrange, choice
import json
import http.client
import time
import redis

class CloudManager(object):
    ARTIK_CLOUD_MESSAGE_URL = 'api.artik.cloud'
    def __init__(self, deviceId, accessToken, tickSecond=10):
        super(CloudManager, self).__init__()
        self.deviceId = deviceId
        self.accessToken = accessToken
        self.tickSecond = tickSecond
    def routine(self):
        headers = {
            'authorization': "Bearer " + self.accessToken,
            'content-type': "application/json",
            }
        payload = dict()
        payload['sdid'] = self.deviceId
        payload['type'] = 'message'

        while True:
            try:
                conn = http.client.HTTPSConnection(self.ARTIK_CLOUD_MESSAGE_URL)
                payload['data'] = '{"Temperature" : '+ str(randrange(1,30)) + ',"Humidity" : ' + str(randrange(0,100)) + ',"Hall" : ' + choice(['true','false']) + '}'

                conn.request("POST", "/v1.1/messages", json.dumps(payload), headers)
                res = conn.getresponse()
                data = res.read()
            except Exception as e:
                print(e)
            time.sleep(self.tickSecond)


if __name__ == '__main__':
    redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
    deviceId = redisClient.get('ArtikDeviceId').decode('utf-8')
    accessToken = redisClient.get('ArtikDeviceAccessToekn').decode('utf-8')
    CloudManager(
        deviceId = deviceId,
        accessToken = accessToken
    ).routine();
