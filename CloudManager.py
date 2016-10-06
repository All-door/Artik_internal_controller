from random import randrange, choice
import json
import http.client
import time
import redis

from HallSensor import HallSensor
from MqSensor import MqSensor

class CloudManager(object):
    ARTIK_CLOUD_MESSAGE_URL = 'api.artik.cloud'
    def __init__(self, hallPin, mqPin, tickSecond=60 * 10):
        super(CloudManager, self).__init__()
        self.tickSecond = tickSecond
        self.redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.hallSensor = HallSensor(hallPin)
        self.mqSensor = MqSensor(mqPin)

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

                    Hall = 'true' if self.hallSensor.getOpened() > 512 else 'false'
                    LPG, CO2, SMOKE = self.mqSensor.getLpgCoSmoke()

                    conn = http.client.HTTPSConnection(self.ARTIK_CLOUD_MESSAGE_URL)
                    payload['data'] = '{"CO2" : '+ str(round(CO2,2)) + ',"SMOKE" : ' + str(round(SMOKE,2)) + ',"LPG" : ' + str(round(LPG,2)) + ',"Hall" : ' + Hall + '}'

                    conn.request("POST", "/v1.1/messages", json.dumps(payload), headers)
                    res = conn.getresponse()
                    data = res.read().decode('utf-8')

                    print ('Artik Cloud Result : ', data)
            except Exception as e:
                print(e)
            time.sleep(self.tickSecond)


if __name__ == '__main__':
    CloudManager(
        hallPin=0,
        mqPin=1
    ).routine();
