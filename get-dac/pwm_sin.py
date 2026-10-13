import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.3
signal_frequency = 10
sampling_frequency = 1000

try:
    dac = pwm.PWM_DAC(12, 10000, dynamic_range=3.3, verbose=False)
    start = time.perf_counter()

    while True:
        t = time.perf_counter() - start
        normalized = sg.get_sin_wave_amplitude(signal_frequency, t)
        dac.set_voltage(amplitude * normalized)

        sg.wait_for_sampling_period(sampling_frequency)

except KeyboardInterrupt:
    print("\nГенерация остановлена поьзователем.")

finally:
    dac.denit()