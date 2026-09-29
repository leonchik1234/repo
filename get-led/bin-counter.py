import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
leds = [16, 12, 25, 17, 27, 23, 22, 24]
GPIO.setup(leds, GPIO.OUT)
arrows = [9, 10]
GPIO.setup(arrows, GPIO.IN)
num = 0

def dec2bin(a):
    return [int(element) for element in bin(a)[2:].zfill(8)]

def update(a):
    bits = dec2bin(a)
    for i in range(len(leds)):
        GPIO.output(leds[i], bits[i])

update(num)

sleep_time = 0.2
last_state_up = 0
last_state_down = 0

while True:
    current_state_up = GPIO.input(9)
    current_state_down = GPIO.input(10)

    if current_state_up > 0 and last_state_up == 0:
        num += 1
        if num > 255:
            num = 0
        print(num, dec2bin(num))
        update(num)
        time.sleep(sleep_time)
    last_state_up = current_state_up

    if current_state_down > 0 and last_state_down == 0:
        num -= 1
        if num < 0:
            num = 0
        print(num, dec2bin(num))
        update(num)
        time.sleep(sleep_time)
    last_state_down = current_state_down

    time.sleep(0.01)




