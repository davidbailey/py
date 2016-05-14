import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
channel = 11
GPIO.setup(channel, GPIO.OUT)

import smbus
from time import sleep
bus = smbus.SMBus(1)
address = 0x48

from time import time

while(True):
  GPIO.output(channel, GPIO.HIGH)
  sleep(0.00028)
  bus.write_i2c_block_data(address, 0x01, [245,131])
  sleep(0.00004)
  GPIO.output(channel, GPIO.LOW)
  sleep(0.0968)
  a3 = bus.read_i2c_block_data(address, 0x00, 2)
  bus.write_i2c_block_data(address, 0x01, [197,131])
  sleep(.01)
  a0 = bus.read_i2c_block_data(address, 0x00, 2)
  bus.write_i2c_block_data(address, 0x01, [213,131])
  sleep(.01)
  a1 = bus.read_i2c_block_data(address, 0x00, 2)
  bus.write_i2c_block_data(address, 0x01, [229,131])
  sleep(.01)
  a2 = bus.read_i2c_block_data(address, 0x00, 2)
  out = [time(), 256 * a0[0] + a0[1], 256 * a1[0] + a1[1], 256 * a2[0] + a2[1], 256 * a3[0] + a3[1]]
  f = open('out.csv', 'a')
  f.write(str(out)[1:-1] + "\n")
  f.close()
  sleep(60)

import pandas
from matplotlib import pyplot

df = pandas.read_csv('out.csv', names=['time','a0','a1','a2','a3'], index_col=0)
df.plot()
pyplot.show()
