import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
led = 26
GPIO.setup(led, GPIO.OUT)
fototrans = 6
GPIO.setup(fototrans, GPIO.IN)

state = 0

while True:
    state = not(GPIO.input(fototrans))
    GPIO.output(led, state)
    time.sleep(0.01)


