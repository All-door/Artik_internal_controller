import time
import sys

class sensor:
	def bin2dec(string_num):
		return str(int(string_num, 2))

	def setup(pin_num):
		pinctl = open("/sys/class/gpio/export", "wb", 0)
		try:
			pinctl. write(str(pin_num))
		except:
			print "Pin " , str(pin_num), " has been exported"
		pinctl.close()

	def set_input(pin_num)	
		filename = '/sys/class/gpio/gpio%d/direction' % pin_num
		pinctldir = open(filename, "wb", 0)
		try:
			pinctldir.write("out")
		except:
			print "Failed to set pin direction"
		pinctldir.close()
	
	def exit_gpio(pin_num):
			pinctl = open("/sys/class/gpio/unexport", "wb", 0)
		try:
			pinctl. write(str(pin_num))
		except:
			print "Pin " , str(pin_num), " has been exported"
		pinctl.close()
	
	data = []
	pinNum = 4

	setup(pinNum)
	set_input(pinNum)

	filename = '/sys/class/gpio/gpio%d/value' % pin_num
	pin = open(filename, "wb", 0)

	pin.write(str(1))
	time.sleep(0.025)

	pin.write(str(0))
	time.sleep(0.02)


	pin = open(filename, "rb", 0)

	for i in range(0,500):
		data.append(pin.read())

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
		print "ERR_RANGE"
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
		print "ERR_RANGE"
		exit(0)

	Humidity = bin2dec(HumidityBit)
	Temperature = bin2dec(TemperatureBit)

	if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:
		print Humidity
		print Temperature
	else:
		print "ERR_CRC"