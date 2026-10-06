import smbus

class MCP4725:
    def __init__(self, dynamic_range, address=0x61, verbose = True):
        self.bus = smbus.SMBus(1)

        self.address = address
        self.wm = 0x00
        self.pds = 0x00

        self.verbose = verbose
        self.dynamic_range = dynamic_range

        self.voltage = 0.0
        self.number = 0

    def deinit(self):
        self.bus.close()
        if self.verbose:
            print("шина I2C закрыта")

    def set_number(self, number):
        if not isinstance(number, int):
            print("На вход ЦАП можно подавать тольео целые числа")
            return
        if not(0 <= number <= 4095):
            print("Число выходит за разрядность MCP4725 (12 бит)")
            return

        first_byte = self.wm | self.pds | (number >> 8)
        second_byte = number & 0xFF
        self.bus.write_byte_data(self.address, first_byte, second_byte)
        self.number = number

        if self.verbose:
            print(f"Число: {number}, отправленные по I2C данные: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n ")

    def set_voltage(self, voltage):
        if not (0 <= voltage <= self.dynamic_range):
            print(f"Напряжение должно быть в диапазоне от 0 до {self.dynamic_range} B")
            return
        
        self.voltage = voltage
        number = int((voltage / self.dynamic_range) * 4095)
        number = max(0, min(4095, number))

        self.set_number(number)

        if self.verbose:
            print(f"Установлено напряжение {voltage:.3f} B (код: {number})\n")

    def get_voltage(self):
        return self.voltage
    def get_number(self):
        return self.number    

if __name__ == "__main__":
    dac = MCP4725(dynamic_range=5.0, address=0x61, verbose=True)

    try:
        while True:
            volt = input("Введите напряжение (В): ").strip()
            try:
                voltage = float(volt)
                dac.set_voltage(voltage)
            except ValueError:
                print("Ошибка введите число\n")

    except KeyboardInterrupt:
        print("\n Программа остановлена пользователем.")
    finally:
        dac.deinit()
