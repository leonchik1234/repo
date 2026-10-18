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

d = read_csv("p5_cases.csv")

algos  = ["bubble", "insertion", "selection", "quick", "heap", "merge"]
cases  = ["random", "sorted", "reversed"]
csty   = {"random": ("black", "-",  "random (avg)"),
          "sorted": ("green", "--", "sorted (best)"),
          "reversed": ("red", ":", "reversed (worst)")}

# ---------- График 1: 6 подграфиков, по алгоритму ----------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for ax, algo in zip(axes, algos):
    for case in cases:
        xs, ys = [], []
        for i in range(len(d["n"])):
            if d["algo"][i] == algo and d["case"][i] == case:
                xs.append(d["n"][i]); ys.append(d["time"][i])
        c, ls, lbl = csty[case]
        ax.plot(xs, ys, color=c, linestyle=ls, label=lbl, linewidth=1.6)
    ax.set_xlabel("N"); ax.set_ylabel("time, s")
    ax.set_title(algo); ax.legend(); ax.grid(True)

plt.tight_layout()
plt.savefig("p5_per_algo.png", dpi=150)
plt.close()

# ---------- График 2: 3 подграфика, по случаю ----------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

for ax, case in zip(axes, cases):
    for algo in algos:
        xs, ys = [], []
        for i in range(len(d["n"])):
            if d["algo"][i] == algo and d["case"][i] == case:
                xs.append(d["n"][i]); ys.append(d["time"][i])
        ax.plot(xs, ys, label=algo, linewidth=1.6)
    ax.set_xlabel("N"); ax.set_ylabel("time, s")
    ax.set_title(f"case: {case}")
    ax.legend(); ax.grid(True)

plt.tight_layout()
plt.savefig("p5_per_case.png", dpi=150)
plt.close()

# ---------- График 3: log-log, по алгоритму ----------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
axes = axes.flatten()

for ax, algo in zip(axes, algos):
    for case in cases:
        xs, ys = [], []
        for i in range(len(d["n"])):
            if d["algo"][i] == algo and d["case"][i] == case:
                xs.append(d["n"][i]); ys.append(d["time"][i])
        c, ls, lbl = csty[case]
        ax.loglog(xs, ys, color=c, linestyle=ls, label=lbl, linewidth=1.6)
    ax.set_xlabel("log N"); ax.set_ylabel("log t")
    ax.set_title(algo + " (log-log)")
    ax.legend(); ax.grid(True, which="both", ls=":")

plt.tight_layout()
plt.savefig("p5_per_algo_loglog.png", dpi=150)
plt.close()

print("Готово: p5_per_algo.png, p5_per_case.png, p5_per_algo_loglog.png")