# Pinout Diagram: https://pinout.xyz
# GPIO - Digital Output from MQ4 (Combustable Gas), MQ7 (CO), HR202 (Humidity) - Connect 3.3V, GND, GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD) # or GPIO.BCM
mode = GPIO.getmode()

channel = 8
GPIO.setup(channel, GPIO.IN) # GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.input(channel)

GPIO.cleanup()

# Serial UART TTL (via CP2102) - EM4100 (125kHz RFID) - Connect 5V, GND, Tx (via CP2102) / Rx (GPIO)
import serial
# s = serial.Serial(port='/dev/ttyUSB0', baudrate=9600) # CP2102
s = serial.Serial(port='/dev/ttyAMA0', baudrate=9600) # https://sites.google.com/site/semilleroadt/raspberry-pi-tutorials/gpio
s.isOpen()

id = []
while True:
  id.append(s.read())
  if id == ['\x00','J','v','O']: break

s.close()

# I2C - BMP180 (Barometer), ADS1115 (4 Channel, 16bit ADC) - Connect 3.3V, GND, SDA, SCL
# sudo apt-get install python-smbus i2c-tools
# echo "
# dtparam=i2c1=on
# dtparam=i2c_arm=on
# " >> /boot/config.txt
# echo "
# i2c-bcm2708 
# i2c-dev
# " >> /etc/modules
# i2cdetect -y 1
import smbus
bus = smbus.SMBus(1)
address = 0x48

bus.write_i2c_block_data(address, 0x01, [197,131])
a0 = bus.read_i2c_block_data(address, 0x00, 2)
bus.write_i2c_block_data(address, 0x01, [213,131])
a1 = bus.read_i2c_block_data(address, 0x00, 2)
bus.write_i2c_block_data(address, 0x01, [229,131])
a2 = bus.read_i2c_block_data(address, 0x00, 2)
bus.write_i2c_block_data(address, 0x01, [245,131])
a3 = bus.read_i2c_block_data(address, 0x00, 2)

# SPI - RC522 (13.56MHz RIFD NFC) - Connect ...
# echo spi-bcm2708 >> /etc/modules
# echo dtparam=spi=on >> /boot/config.txt
# apt-get install python-pip
# pip install spi 
import spi
s = spi.SPI("/dev/spidev0.0")

s.read(1000)

# SPI - nRF24L01 (2.4GHz Tranceiver) - http://tmrh20.github.io/RF24/
