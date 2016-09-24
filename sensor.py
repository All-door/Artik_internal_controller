import time
import sys

class Sensor:
	def bin2dec(string_num):
		return str(int(string_num, 2))

	data = []
	pinNum = 4
	
	def setup(pinNum):
		pinctl = open("/sys/class/gpio/export", "wb", 0)
		try:
			pinctl. write(str(pinNum))
		except:
			print ("Pin " , str(pinNum), " has been exported")
		pinctl.close()

	setup(pinNum)
	
	def set_input(pinNum):	
		filename = '/sys/class/gpio/gpio%d/direction' % pinNum
		pinctldir = open(filename, "wb", 0)
		try:
			pinctldir.write("out")
		except:
			print ("Failed to set pin direction")
		pinctldir.close()
	
	set_input(pinNum)

	filename = '/sys/class/gpio/gpio%d/value' % pinNum
	pin = open(filename, "wb", 0)

	def exit_gpio(pinNum):
		pinctl = open("/sys/class/gpio/unexport", "wb", 0)
		try:
			pinctl.write(str(pinNum))
		except:
			print ("Pin " , str(pinNum), " has been exported")
		pinctl.close()
	
	
	pin.write(str(1))
	time.sleep(0.025)

	pin.write(str(0))
	time.sleep(0.02)

	pin.close()
	exit_gpio()
	
	for i in range(0,500):
		pin = open(filename, "rb", 0)
		data.append(pin.read())
		pin.close()

	exit_gpio()
	
	bit_count = 0
	tmp = 0
	count = 0
	HumidityBit = ""
	TemperatureBit = ""
	crc = ""

	try:
		while data[count] == 1:
			tmp = 1
			count = count + 1

		for i in range(0, 32):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "1"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "1"
			else:
				if i>=0 and i<8:
					HumidityBit = HumidityBit + "0"
				if i>=16 and i<24:
					TemperatureBit = TemperatureBit + "0"

	except:
		print ("ERR_RANGE")
		exit(0)

	try:
		for i in range(0, 8):
			bit_count = 0

			while data[count] == 0:
				tmp = 1
				count = count + 1

			while data[count] == 1:
				bit_count = bit_count + 1
				count = count + 1

			if bit_count > 3:
				crc = crc + "1"
			else:
				crc = crc + "0"
	except:
		print ("ERR_RANGE")
		exit(0)

	Humidity = bin2dec(HumidityBit)
	Temperature = bin2dec(TemperatureBit)
	def getTemperature():
		if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
			return Temperature
		else:
			return "ERR_CRC"
			
	def getHumidity():
		if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
			return Humidity
		else:
			return "ERR_CRC"