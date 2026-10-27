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
        """
        # Читаем 2 байта (16-битное слово)
        data = self.bus.read_word_data(self.address, 0)

        # ВАЖНО: Raspberry Pi (smbus) читает байты в формате Little-Endian.
        # Это значит, что первый байт от микросхемы попадает в МЛАДШИЙ разряд.
        
        # 1. Отделяем байты, как их реально видит smbus:
        byte_0 = data & 0xFF       # Это первый байт, пришедший по шине (старшие 8 бит числа)
        byte_1 = (data >> 8) & 0xFF # Это второй байт (младшие 2 бита + 6 нулей)

        # 2. Собираем 10-битное число по даташиту:
        # Старшие 8 бит сдвигаем на 6 позиций влево.
        # Младшие 2 бита (они находятся в старших разрядах второго байта) сдвигаем на 2 позиции вправо.
        number = (byte_0 << 6) | (byte_1 >> 2)

        if self.verbose:
            print(f"Сырые данные: {data:04X}, "
                  f"Байт 0 (старший): {byte_0:02X}, "
                  f"Байт 1 (младший): {byte_1:02X}, "
                  f"Число: {number}")

        return number

    def get_voltage(self):
        """
        Возвращает измеренное напряжение в вольтах.
        """
        number = self.get_number()
        # Делим на 1024 (полное количество шагов 10-битного АЦП)
        # Это точнее математически, чем деление на 1023.
        voltage = (number / 1024.0) * self.dynamic_range
        return voltage


if __name__ == "__main__":
    # ВНИМАНИЕ: Перемычка на блоке AUX должна быть на 5V! 
    # Если питание 3.3V, укажи dynamic_range=3.3
    adc = MCP3021(dynamic_range=5.0, verbose=True) # Включил verbose для отладки

    try:
        while True:
            voltage = adc.get_voltage()
            print(f"Измеренное напряжение: {voltage:.3f} В\n")
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nИзмерение остановлено пользователем.")

    finally:
        adc.deinit()