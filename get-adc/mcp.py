import mcp3021_driver as mcp
import adc_plot
import time


# Параметры эксперимента
duration = 10.0
dynamic_range = 5.0      # замерить мультиметром на PWR блока AUX (5V)


voltage_values = []
time_values = []


try:
    adc = mcp.MCP3021(dynamic_range=dynamic_range, verbose=False)

    start_time = time.perf_counter()

    while time.perf_counter() - start_time < duration:
        voltage = adc.get_voltage()
        voltage_values.append(voltage)
        time_values.append(time.perf_counter() - start_time)

    # График напряжения от времени
    adc_plot.plot_voltage_vs_time(time_values, voltage_values, dynamic_range)

    # Гистограмма периодов измерений
    adc_plot.plot_sampling_period_hist(time_values)

except KeyboardInterrupt:
    print("\nЭксперимент прерван пользователем.")

finally:
    adc.deinit()