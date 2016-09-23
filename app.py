from flask import Flask, render_template
import jinja2
import os
from SettingParser import SettingParser

ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), './template')
app = Flask(__name__, template_folder=ASSET_DIR, static_folder=ASSET_DIR)
settingParser = SettingParser()

templateLoader = jinja2.FileSystemLoader(searchpath="/")
templateEnv = jinja2.Environment(loader=templateLoader)

template = templateEnv.get_template("/root/Artik_internal_controller/template/index.html")

@app.route('/')
def loadPage():
    data = settingParser.read()
    print(data['SSID'])    
    return template.render(data=data)


@app.route('/save/<ssid>/<password>/<deviceId>/<cloudId>/<masterPw>')
def save(ssid, password, deviceId, cloudId, masterPw):
    data = settingParser.read()
    data['SSID'] = ssid
    data['PASSWORD'] = password
    data['ALL_DOOR_ID'] = deviceId
    data['ARTIK_CLOUD_ID'] = cloudId
    data['MASTER_PW'] = masterPw
    settingParser.write(data)

    os.system("wpa_passphrase " + data['SSID'] + " " + data['PASSWORD']+ " > /etc/wpa_supplicant/wpa_supplicant.conf")

    data = settingParser.read()
    exit()
    return template.render(data=data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
