import smbus
import time


class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        """Освобождает I2C-шину."""
        self.bus.close()

    def get_number(self):
        """
        Читает 10-битное число из MCP3021.
        Используем read_i2c_block_data, чтобы гарантировать порядок байтов:
        0-й байт — старший, 1-й байт — младший.
        """
        # Читаем 2 байта подряд
        data = self.bus.read_i2c_block_data(self.address, 0, 2)

        upper_byte = data[0] # Старшие 8 бит
        lower_byte = data[1] # Младшие 2 бита + нули

        # Собираем 10-битное число по даташиту MCP3021:
        # Старший байт сдвигаем влево на 6, 
        # младший сдвигаем вправо на 2 (чтобы отбросить нули).
        number = (upper_byte << 6) | (lower_byte >> 2)

        if self.verbose:
            print(f"Байты: {upper_byte:02X} {lower_byte:02X}, "
                  f"Число: {number}")

        return number

    def get_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах.
        Формула: U = number / 1024 * dynamic_range
        """
        number = self.get_number()
        # Для 10-битного АЦП используем деление на 1024 (2^10)
        voltage = (number / 1024.0) * self.dynamic_range
        return voltage


if __name__ == "__main__":
    # Обязательно проверь мультиметром напряжение на пине PWR блока AUX (должно быть ~5.0В)
    adc = MCP3021(dynamic_range=5.0, verbose=True) # Включаем лог для проверки

    try:
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение: {voltage:.3f} В\n")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")

    finally:
        adc.deinit()