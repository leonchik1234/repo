import RPi.GPIO as GPIO
import time


class R2R_ADC:
    def __init__(self, dynamic_range, compare_time=0.01, verbose=False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time

        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial=0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()

    def number_to_dac(self, number):
        number &= 0xFF
        for i, pin in enumerate(self.bits_gpio):
            bit = (number >> (7 - i)) & 1
            GPIO.output(pin, bit)

    def sequential_counting_adc(self):
        max_number = 255
        for number in range(max_number + 1):
            self.number_to_dac(number)
            time.sleep(self.compare_time)
            if GPIO.input(self.comp_gpio) == 1:
                return number
        return max_number

    def get_sc_voltage(self):
        code = self.sequential_counting_adc()
        return code / 255 * self.dynamic_range

    def successive_approximation_adc(self):
        """
        АЦП последовательного приближения (SAR).

        Бинарный поиск по коду 0..255. На каждом шаге:
        - выставляем в проверяемом бите 1,
        - ждём compare_time,
        - читаем компаратор:
            * 1 → U_ЦАП > U_вход, бит надо сбросить в 0;
            * 0 → U_ЦАП < U_вход, бит остаётся 1.

        За 8 итераций находим код, ближайший снизу к входному напряжению.
        """
        result = 0

        # Перебираем биты от старшего (7) к младшему (0)
        for bit_index in range(7, -1, -1):
            # Пробуем установить текущий бит
            trial = result | (1 << bit_index)

            self.number_to_dac(trial)
            time.sleep(self.compare_time)

            comparator_value = GPIO.input(self.comp_gpio)

            if self.verbose:
                voltage = trial / 255 * self.dynamic_range
                print(f"Бит {bit_index}: пробуем код {trial} "
                      f"({voltage:.3f} В), компаратор: {comparator_value}")

            if comparator_value == 0:
                # U_ЦАП < U_вход → пробуемый бит подходит, оставляем его
                result = trial
            # Иначе (1): U_ЦАП > U_вход → бит не подходит, остаётся 0

        return result

    def get_sar_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах,
        полученное методом последовательного приближения.
        """
        code = self.successive_approximation_adc()
        return code / 255 * self.dynamic_range


if __name__ == "__main__":
    # dynamic_range предварительно измерить мультиметром!
    adc = R2R_ADC(dynamic_range=3.3, verbose=False)

    try:
        while True:
            voltage = adc.get_sar_voltage()
            print(f"Измеренное напряжение (SAR): {voltage:.3f} В")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")

    finally:
        adc.deinit()