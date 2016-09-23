from flask import Flask, render_template
from jinja2 import Template
from SettingParser import SettingParser

app = Flask(__name__)
settingParser = SettingParser()


@app.route('/')
def loadPage():
    data = settingParser.read()

    ssid = data['SSID']
    pw = data['PASSWORD']
    deviceId = data['DEVICE_ID']
    cloudId = data['CLOUD_ID']
    ap_pw = data['MASTER_PW']
    
    return render_template('./softAP/index.html', data)


@app.route('/save/<ssid>/<password>/<deviceId>/<cloudId>/<masterPw>')
def save(ssid, password, deviceId, cloudId, masterPw):
    data = settingParser.read()
    data['SSID'] = ssid
    data['PASSWORD'] = password
    data['DEVICE_ID'] = deviceId
    data['CLOUD_ID'] = cloudId
    data['MASTER_PW'] = masterPw
    settingParser.write(data)
    return settingParser.read()['SSID']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
