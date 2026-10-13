import r2r_dac as r2r
import signal_generator as sg

amplitude = 3.0
signal_frequency = 10
sampling_frequency = 1000

gpio_bits = [16, 20, 21, 25, 26, 17, 27, 22]
dac = None

try:
    dac = r2r.R2R_DAC(gpio_bits = gpio_bits, dynamic_range=3.1, verbose=False)

    t = 0.0

    while True:
        normalized = sg.get_sin_wave_amplitude(signal_frequency, t)

        voltage = amplitude * normalized
        dac.set_voltage(voltage)

        sg.wait_for_sampling_period(sampling_frequency)

        t += 1.0 / sampling_frequency

except KeyboardInterrupt:
    print("\nГенерация остановлена поьзователем.")

finally:
    dac.denit()
