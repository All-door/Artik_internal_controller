class SettingParser:

    filePath='./info.txt'

    def read(self):
        f = open(self.filePath, 'r')
        info = dict()

        lines = f.readlines()
        for line in lines:
            if not line: continue
            if '=' not in line: continue
            if '#' == line[0]: continue

            key = line.split('=')[0]
            data = line.split('=')[1].split(';')[0]

            info[key] = data
        f.close()
        return info

    def write(self, info):
        f = open(self.filePath, 'r')
        
        lines = f.readlines()
        f.close()
        f = open(self.filePath, 'w')
        for line in lines:
            if not line or '=' not in line or '#' == line[0]:
                f.write(line)
                continue

            key = line.split('=')[0]
            data = line.split('=')[1].split(';')[0]
            if key in info:
                line = key + '=' + info[key] + '\n'
                f.write(line)

        f.close()

if __name__ == '__main__':
    settingParser = SettingParser()

    data = settingParser.read();
    print(data)

    data['SSID']='newSSID'
    print(data)
    settingParser.write(data)
   
