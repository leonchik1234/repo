import time
import random
import csv
import numpy as np
import matplotlib.pyplot as plt

# ==================== СОРТИРОВКИ ====================

def bubble_sort(a):
    n = len(a)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]

def insertion_sort(a):
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def selection_sort(a):
    n = len(a)
    for i in range(n - 1):
        m = i
        for j in range(i + 1, n):
            if a[j] < a[m]:
                m = j
        a[i], a[m] = a[m], a[i]

# ==================== ЗАМЕРЫ PYTHON ====================

def measure_python():
    random.seed(42)
    rows = [["n", "bubble", "insertion", "selection"]]

    for n in range(200, 20001, 200):
        base = [random.randint(-100000, 100000) for _ in range(n)]
        row = [n]
        for fn in (bubble_sort, insertion_sort, selection_sort):
            a = base.copy()
            t = time.perf_counter()
            fn(a)
            row.append(time.perf_counter() - t)
        rows.append(row)
        print(f"python {n} done")

    with open("p4_python.csv", "w", newline="") as f:
        csv.writer(f).writerows(rows)

# ==================== ЧТЕНИЕ CSV ====================

def read_csv(path):
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        data = {h: [] for h in header}
        for row in r:
            for h, v in zip(header, row):
                data[h].append(float(v))
        return {k: np.array(v) for k, v in data.items()}

# ==================== ГРАФИКИ ====================

def plot_all():
    cpp = read_csv("p4_cpp.csv")
    py  = read_csv("p4_python.csv")

    # --- 1. Обычный масштаб, три подграфика ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, algo in zip(axes, ("bubble", "insertion", "selection")):
        ax.plot(cpp["n"], cpp[algo], 'b-o', markersize=3, label="C++ (-O2)")
        ax.plot(py["n"],  py[algo],  'r-s', markersize=3, label="Python")
        ax.set_xlabel("N"); ax.set_ylabel("time, s")
        ax.set_title(algo); ax.legend(); ax.grid(True)
    plt.tight_layout()
    plt.savefig("p4_linear.png", dpi=150)
    plt.close()

    # --- 2. log-log ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, algo in zip(axes, ("bubble", "insertion", "selection")):
        ax.loglog(cpp["n"], cpp[algo], 'b-o', markersize=3, label="C++ (-O2)")
        ax.loglog(py["n"],  py[algo],  'r-s', markersize=3, label="Python")
        ax.set_xlabel("log N"); ax.set_ylabel("log t")
        ax.set_title(algo + " (log-log)")
        ax.legend(); ax.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig("p4_loglog.png", dpi=150)
    plt.close()

    # --- 3. Отношение Python / C++ ---
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))
    for ax, algo in zip(axes, ("bubble", "insertion", "selection")):
        cpp_interp = np.interp(py["n"], cpp["n"], cpp[algo])
        ax.plot(py["n"], py[algo] / cpp_interp, 'k-o', markersize=3)
        ax.set_xlabel("N"); ax.set_ylabel("Python / C++")
        ax.set_title(algo + ": во сколько раз Python медленнее")
        ax.grid(True)
    plt.tight_layout()
    plt.savefig("p4_ratio.png", dpi=150)
    plt.close()

    print("Готово: p4_linear.png, p4_loglog.png, p4_ratio.png")

# ==================== MAIN ====================

if __name__ == "__main__":
    measure_python()
    plot_all()