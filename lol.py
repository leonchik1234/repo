import xml.dom.minidom
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# 1. Парсим XML файл
doc = xml.dom.minidom.parse('Co_60')

# 2. Извлекаем все значения из тегов <energy>
energy_tags = doc.getElementsByTagName('energy')
energies = []

for tag in energy_tags:
    try:
        val = float(tag.firstChild.data.strip())
        energies.append(val)  # <--- теперь работает
    except (AttributeError, ValueError):
        continue

energies = np.array(energies)
print(f"Загружено {len(energies)} значений энергии")
print(f"Диапазон: от {energies.min():.6f} до {energies.max():.6f}")

# 3. Построение графика
fig, ax = plt.subplots(figsize=(10, 6))

ax.hist(energies, bins=30, density=True,
        alpha=0.6, color='skyblue', edgecolor='black',
        label='Гистограмма')

kde = gaussian_kde(energies)
x_grid = np.linspace(energies.min(), energies.max(), 200)
ax.plot(x_grid, kde(x_grid), 'r-', linewidth=2, label='Плотность (KDE)')

ax.set_xlabel('Энергия гамма-квантов (отн. ед.)')
ax.set_ylabel('Плотность вероятности')
ax.set_title('Распределение частиц по энергиям (данные Co-60)')
ax.legend()
ax.grid(alpha=0.3, linestyle='--')

plt.tight_layout()
plt.show()