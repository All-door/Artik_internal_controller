import json
import time
import redis

class CloudManager(object):
    ARTIK_CLOUD_URL = '';
    def __init__(self, deviceId, redisUrl='localhost', redisPort=6379, tickSecond=30):
        super(CloudManager, self).__init__()
        self.deviceId = deviceId
        self.redisUrl = redisUrl
        self.redisPort = redisPort
        self.tickSecond = tickSecond

    def routine(self):
        while True:
            try:
                print('Rotuine')
            except Exception as e:
                print(e)
            time.sleep(self.tickSecond)


if __name__ == '__main__':
    CloudManager("").routine();
