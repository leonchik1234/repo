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
                if h == "time":
                    data[h].append(float(v))
                elif h == "n":
                    data[h].append(int(v))
                else:
                    data[h].append(v)
        return data

d = read_csv("p8_types.csv")

types = ["char", "short", "int", "long", "longlong", "Light", "Heavy"]
colors = {
    "char":     "red",
    "short":    "orange",
    "int":      "gold",
    "long":     "green",
    "longlong": "blue",
    "Light":    "purple",
    "Heavy":    "black",
}

# ---------- 1. Все типы на одном графике ----------
plt.figure(figsize=(10, 6))
for t in types:
    xs, ys = [], []
    for i in range(len(d["n"])):
        if d["type"][i] == t:
            xs.append(d["n"][i]); ys.append(d["time"][i])
    plt.plot(xs, ys, color=colors[t], label=t, linewidth=1.7)

plt.xlabel("N")
plt.ylabel("time, s")
plt.title("Sorting different data types")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p8_types.png", dpi=150)
plt.close()

# ---------- 2. Только числовые типы, чтобы разница была видна ----------
plt.figure(figsize=(10, 6))
for t in ("char", "short", "int", "long", "longlong"):
    xs, ys = [], []
    for i in range(len(d["n"])):
        if d["type"][i] == t:
            xs.append(d["n"][i]); ys.append(d["time"][i])
    plt.plot(xs, ys, color=colors[t], label=t, linewidth=1.7)

plt.xlabel("N")
plt.ylabel("time, s")
plt.title("Numeric types only")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p8_numeric.png", dpi=150)
plt.close()

# ---------- 3. Структуры отдельно ----------
plt.figure(figsize=(10, 6))
for t in ("Light", "Heavy"):
    xs, ys = [], []
    for i in range(len(d["n"])):
        if d["type"][i] == t:
            xs.append(d["n"][i]); ys.append(d["time"][i])
    plt.plot(xs, ys, color=colors[t], label=t, linewidth=1.7)

plt.xlabel("N")
plt.ylabel("time, s")
plt.title("Structures: Light vs Heavy")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p8_structs.png", dpi=150)
plt.close()

# ---------- 4. Нормировка: время / (N log N) — сравнение констант ----------
plt.figure(figsize=(10, 6))
for t in types:
    xs, ys = [], []
    for i in range(len(d["n"])):
        if d["type"][i] == t:
            n = d["n"][i]
            xs.append(n); ys.append(d["time"][i] / (n * np.log2(n)))
    plt.plot(xs, ys, color=colors[t], label=t, linewidth=1.7)

plt.xlabel("N")
plt.ylabel("t / (N log2 N)")
plt.title("Константы: во сколько раз тип тяжелее")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p8_constants.png", dpi=150)
plt.close()

print("Готово: p8_types.png, p8_numeric.png, p8_structs.png, p8_constants.png")