import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
GPIO.output(leds, 0)
arrows = [9, 10]
GPIO.setup(arrows, GPIO.IN)
num = 0
sleep_time = 0.2

def dec2bin(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]
def update(a):
    bits = dec2bin(a)
    for i in range(len(leds)):
        GPIO.output(leds[i], bits[i])


while True:
    if  not GPIO.input(9):
        num += 1
        if num > 255: num = 255
        update(num)
        time.sleep(sleep_time)
    elif not GPIO.input(10):
        num -= 1
        if num < 0: num = 0
        update(num)
        time.sleep(speep_time)
    time.sleep(0.01)
    GPIO.output(leds, dec2bin(num))
