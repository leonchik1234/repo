import matplotlib.pyplot as plt


def plot_voltage_vs_time(time, voltage, max_voltage):
    """
    Строит график зависимости напряжения от времени и сохраняет его в файл.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)

    plt.title("Зависимость напряжения от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")

    plt.xlim(time[0], time[-1] if len(time) > 1 else time[0] + 1)
    plt.ylim(0, max_voltage)

    plt.grid(True)
    
    # СОХРАНЕНИЕ ГРАФИКА В ФАЙЛ
    plt.savefig("voltage_plot.png", dpi=300)
    print("График напряжения сохранен в файл voltage_plot.png")
    
    plt.show()


def plot_sampling_period_hist(time):
    """
    Строит распределение количества измерений по их продолжительности и сохраняет в файл.
    """
    sampling_periods = []
    for i in range(1, len(time)):
        sampling_periods.append(time[i] - time[i - 1])

    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods)

    plt.title("Распределение периодов измерений")
    plt.xlabel("Период измерения, с")
    plt.ylabel("Количество измерений")

    plt.xlim(0, 0.06) # Если строишь для MCP3021, лучше поменять на plt.xlim(0, 0.005)
    plt.grid(True)
    
    # СОХРАНЕНИЕ ГИСТОГРАММЫ В ФАЙЛ
    plt.savefig("histogram_plot.png", dpi=300)
    print("Гистограмма сохранена в файл histogram_plot.png")
    
    plt.show()