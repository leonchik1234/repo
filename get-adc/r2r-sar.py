import r2r_adc as adc
import time
import adc_plot


# Параметры эксперимента
duration = 3.0
dynamic_range = 3.3         # измерить мультиметром!


voltage_values = []
time_values = []


try:
    my_adc = adc.R2R_ADC(dynamic_range=dynamic_range,
                         compare_time=0.001,
                         verbose=False)

    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration:
        voltage = my_adc.get_sar_voltage()
        voltage_values.append(voltage)
        time_values.append(time.perf_counter() - start_time)

    # График напряжения от времени
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

    # Гистограмма периодов измерений
    adc_plot.plot_sampling_period_hist(time_values)

except KeyboardInterrupt:
    print("\nЭксперимент прерван пользователем.")

finally:
    my_adc.deinit()