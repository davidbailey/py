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
# Based on https://github.com/dhhagan/Adafruit-Raspberry-Pi-Python-Code/blob/master/ADS1115/__init__.py
# pip install adafruit-python
import smbus
from time import sleep
bus = smbus.SMBus(1)
a2d_address = 0x48
bmp085_address = 0x77

bus.write_i2c_block_data(a2d_address, 0x01, [197,131])
sleep(.01)
a0 = bus.read_i2c_block_data(a2d_address, 0x00, 2)
bus.write_i2c_block_data(a2d_address, 0x01, [213,131])
sleep(.01)
a1 = bus.read_i2c_block_data(a2d_address, 0x00, 2)
bus.write_i2c_block_data(a2d_address, 0x01, [229,131])
sleep(.01)
a2 = bus.read_i2c_block_data(a2d_address, 0x00, 2)
bus.write_i2c_block_data(a2d_address, 0x01, [245,131])
sleep(.01)
a3 = bus.read_i2c_block_data(a2d_address, 0x00, 2)

import Adafruit_BMP.BMP085 as BMP085
bmp085 = BMP085.BMP085()

temperature = bmp085.read_temperature()
pressure = bmp085.read_pressure()
altitude = bmp085.read_altitude()
sealevel_pressure = bmp085.read_sealevel_pressure()

out = [time(), 256 * a0[0] + a0[1], 256 * a1[0] + a1[1], 256 * a2[0] + a2[1], 256 * a3[0] + a3[1], temperature, pressure, altitude, sealevel_pressure]
# echo "a0, a1, a2, a3" > out.csv
f = open('out.csv', 'a')
f.write(str(out)[1:-1] + "\n")
f.close()


# Sharp GP2Y1010AU0F (Optical Dust Sensor) - Connect ...
# http://www.howmuchsnow.com/arduino/airquality/
# https://github.com/PaulZC/GP2Y1010AU0F_Dust_Sensor
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
channel = 11
GPIO.setup(channel, GPIO.OUT)

import smbus
from time import sleep
bus = smbus.SMBus(1)
address = 0x48

while(True):
  GPIO.output(channel, GPIO.LOW)
  bus.write_i2c_block_data(address, 0x01, [229,131])
  sleep(0.00028)
  a2 = bus.read_i2c_block_data(address, 0x00, 2)
  sleep(0.00004)
  GPIO.output(channel, GPIO.HIGH)
  sleep(0.0968)
  print(a2[0]*256 + a2[1])


# SPI - RC522 (13.56MHz RIFD NFC) - Connect ...
# echo spi-bcm2708 >> /etc/modules
# echo dtparam=spi=on >> /boot/config.txt
# apt-get install python-pip
# pip install spi 
import spi
s = spi.SPI("/dev/spidev0.0")

s.read(1000)

# SPI - nRF24L01 (2.4GHz Tranceiver) - http://tmrh20.github.io/RF24/

