import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, gpio_bits, dynamic_range, verbose=False):
        self.gpio_bits = gpio_bits
        self.dynamic_range = dynamic_range
        self.verbose = verbose

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_bits, GPIO.OUT)

    def denit(self):
        GPIO.output(self.gpio_bits, 0)
        GPIO.cleanup()
    
    def set_number(self, number):
        if not(0 <= number <= 255):
            if self.verbose:
                print("Число выходит за диапазон 8-bit ЦАП (0 - 255")
                print("Устанавливаем 0")
            number = 0
        binary = f"{number:08b}"

        for i, bit in enumerate(binary):
            GPIO.output(self.gpio_bits[i], int(bit))

        if self.verbose:
            print(f"Установлено число: {number} ({binary})")
    
    def set_voltage(self, voltage):
        if not (0.0 <= voltage <= self.dynamic_range):
            if self.verbose:
                print(f"Напряжение выходит за динамический диапазон ЦАП "
                      f"(0.00 - {self.dynamic_range:.2f} B)" )
                print("Устанавливаем 0.0 В")
            number = 0
        else:
            number = int(voltage / self.dynamic_range * 255)

        self.set_number(number)

if __name__ == "__main__":
    dac = None
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.17, True)
        
        while True:
            try:
                voltage = float(input("Введите напряжение в вольтах:"))
                dac.set_voltage(voltage)

            except ValueError:
                print("Вы ввели не число. Попробуйте еще раз\n")

    finally:
        if dac is not None:
            dac.denit()