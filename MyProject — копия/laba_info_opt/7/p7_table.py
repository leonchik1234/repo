import csv
import numpy as np
import matplotlib.pyplot as plt

def read_csv(path):
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        data = {h: [] for h in header}
        for row in r:
            for h, v in zip(header, row):
                data[h].append(float(v))
        return {k: np.array(v) for k, v in data.items()}

algos = ["bubble", "insertion", "selection", "quick", "heap", "merge"]
colors = {
    "bubble":    "red",
    "insertion": "orange",
    "selection": "gold",
    "quick":     "green",
    "heap":      "blue",
    "merge":     "purple",
}

cpp = read_csv("7_pic/p7_small.csv")
py  = read_csv("7_pic/p7_small_py.csv")

# ---------- 1. C++ на маленьких N ----------
plt.figure(figsize=(9, 5.5))
for algo in algos:
    plt.plot(cpp["n"], cpp[algo] * 1e9, color=colors[algo],
             label=algo, linewidth=1.5)   # переводим в наносекунды
plt.xlabel("N")
plt.ylabel("time, ns")
plt.title("Small N (3..100) — C++ -O2")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p7_cpp.png", dpi=150)
plt.close()

# ---------- 2. C++ vs Python на маленьких N ----------
# На одном графике сложно — Python в 50 раз медленнее.
# Разделим: слева C++, справа Python.
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

for ax, d, title, scale in (
    (axes[0], cpp, "C++ -O2", 1e9),
    (axes[1], py,  "Python",  1e6),     # Python — в микросекундах
):
    for algo in algos:
        ax.plot(d["n"], d[algo] * scale, color=colors[algo],
                label=algo, linewidth=1.5)
    ax.set_xlabel("N")
    ax.set_ylabel("time (ns)" if scale == 1e9 else "time, µs")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.savefig("p7_cpp_vs_py.png", dpi=150)
plt.close()

# ---------- 3. Отношение Python / C++ ----------
plt.figure(figsize=(9, 5.5))
for algo in algos:
    # интерполируем C++ на сетку Python (у них одинаковые N — 3..100)
    cpp_interp = np.interp(py["n"], cpp["n"], cpp[algo])
    ratio = py[algo] / cpp_interp
    plt.plot(py["n"], ratio, color=colors[algo], label=algo, linewidth=1.5)

plt.xlabel("N")
plt.ylabel("Python / C++")
plt.title("Во сколько раз Python медленнее C++ (N = 3..100)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p7_ratio.png", dpi=150)
plt.close()

print("Готово: p7_cpp.png, p7_cpp_vs_py.png, p7_ratio.png")