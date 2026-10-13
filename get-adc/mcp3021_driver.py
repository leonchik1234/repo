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

        Микросхема отдаёт результат в 16-битном слове, но 10 значащих бит
        лежат не в самом младшем разряде, а со сдвигом: старший байт содержит
        биты 9..2 (старшие 8 из 10), младший байт — биты 1..0 в старших
        разрядах байта (после сдвига вправо на 2, с отбрасыванием «мусорных»
        нулей в младших разрядах).
        """
        data = self.bus.read_word_data(self.address, 0)

        # smbus.read_word_data возвращает слово в little-endian:
        # младший байт данных оказывается в старшем байте результата
        # и наоборот. Поэтому меняем их местами:
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF

        # Собираем 10-битное число:
        # старший байт сдвигаем влево на 6, младший — вправо на 2,
        # чтобы отбросить два младших бита (они всегда 0)
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)

        if self.verbose:
            print(f"Принятые данные: {data}, "
                  f"Старший байт: {upper_data_byte:x}, "
                  f"Младший байт: {lower_data_byte:x}, "
                  f"Число: {number}")

        return number

    def get_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах.
        Формула: U = number / (2^10 - 1) * dynamic_range
        """
        number = self.get_number()
        voltage = number / 1023 * self.dynamic_range
        return voltage


if __name__ == "__main__":
    # dynamic_range нужно предварительно измерить мультиметром
    # на контакте PWR блока AUX при включённой перемычке на 5V
    adc = MCP3021(dynamic_range=5.0, verbose=False)

    try:
        while True:
            voltage = adc.get_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")

    finally:
        adc.deinit()