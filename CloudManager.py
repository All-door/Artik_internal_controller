from random import randrange, choice
import json
import http.client
import time
import redis

class CloudManager(object):
    ARTIK_CLOUD_MESSAGE_URL = 'api.artik.cloud'
    def __init__(self, tickSecond=60 * 10):
        super(CloudManager, self).__init__()
        self.tickSecond = tickSecond
        self.redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)

    def routine(self):
        while True:
            try:
                deviceId = self.redisClient.get('ArtikDeviceId').decode('utf-8')
                accessToken = self.redisClient.get('ArtikDeviceAccessToekn').decode('utf-8')

                if deviceId == 'None' or accessToken == 'None':
                    print('DevcieID, AccessToken is None')
                else:
                    headers = {
                        'authorization': "Bearer " + accessToken,
                        'content-type': "application/json",
                        }
                    payload = dict()
                    payload['sdid'] = deviceId
                    payload['type'] = 'message'

                    conn = http.client.HTTPSConnection(self.ARTIK_CLOUD_MESSAGE_URL)
                    payload['data'] = '{"CO2" : '+ str(randrange(1,30)) + ',"SMOKE" : ' + str(randrange(0,100))+ ',"LPG" : ' + str(randrange(0,100)) + ',"Hall" : ' + choice(['true','false']) + '}'

                    conn.request("POST", "/v1.1/messages", json.dumps(payload), headers)
                    res = conn.getresponse()
                    data = res.read()
            except Exception as e:
                print(e)
            time.sleep(self.tickSecond)


if __name__ == '__main__':
    CloudManager().routine();
