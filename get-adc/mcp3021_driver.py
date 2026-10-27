import smbus
import time


class MCP3021:
    """Драйвер 10-битного АЦП MCP3021 на шине I2C."""

    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        """Освобождает шину I2C."""
        self.bus.close()

    def get_number(self):
        """Читает из MCP3021 10-битное число."""
        data = self.bus.read_word_data(self.address, 0)

        # Байт, пришедший по шине вторым (младший по порядку передачи)
        lower_data_byte = data >> 8
        # Байт, пришедший по шине первым (старший по порядку передачи)
        upper_data_byte = data & 0xFF

        # Согласно документации MCP3021:
        #   D9..D2 — в первом принятом байте (upper)
        #   D1..D0 — в старших битах второго байта (lower)
        # Итоговое 10-битное значение:
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        if self.verbose:
            print(
                f"Принятые данные: {data}, "
                f"Старший байт: {upper_data_byte:x}, "
                f"Младший байт: {lower_data_byte:x}, "
                f"Число: {number}"
            )

        return number

    def get_voltage(self):
        """Возвращает измеренное напряжение в Вольтах."""
        number = self.get_number()
        # 10-битный АЦП: 2**10 = 1024 уровня
        voltage = number * self.dynamic_range / 1024
        return voltage


if __name__ == "__main__":
    # Динамический диапазон (опорное напряжение) нужно измерить мультиметром
    # на контакте PWR блока AUX при включённой перемычке на 5V.
    DYNAMIC_RANGE = 3.3  # заменить на измеренное значение, В

    adc = None
    try:
        adc = MCP3021(dynamic_range=DYNAMIC_RANGE, verbose=False)
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")
    finally:
        if adc is not None:
            adc.deinit()