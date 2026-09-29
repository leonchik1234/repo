import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
dac_pins = [16, 20, 21, 25, 26, 17, 27, 22]
for pin in dac_pins:
    GPIO.setup(pin, GPIO.OUT) 

dynamic_range = 3.17
def voltage_to_number(voltage):
    if not(0.0 <= voltage <= dynamic_range):
        print("Напряжение выходит за динамический диапазон ЦАП (0.00 - 3.17 B)")
        print("Устанавливаем 0.0 В")
        return 0
    return int(voltage / dynamic_range * 255)

def number_to_dac(a):
    bin = f"{a:08b}"
    for i, bit in enumerate(bin):
        GPIO.output(dac_pins[i], int(bit))

try:
    while True:
        try:
            voltage = float(input("Введите напряжение в Вольтах: "))
            number = voltage_to_number(voltage)
            number_to_dac(number)
        except ValueError:
            print("Вы ввели не число. Попробуйте еще раз\n")

finally:
    number_to_dac(0)
    GPIO.cleanup()