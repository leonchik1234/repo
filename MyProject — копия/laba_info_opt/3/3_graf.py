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

for tag in ("O0", "O1", "O2", "O3"):
    d = read_csv(f"p3_{tag}.csv")
    n = d["n"]

    plt.figure(figsize=(9, 5.5))
    for algo in algos:
        # фильтруем -1 (заглушки для O(N^2) на больших N)
        mask = d[algo] >= 0
        plt.plot(n[mask], d[algo][mask], color=colors[algo],
                 label=algo, linewidth=1.6)

    plt.xlabel("N")
    plt.ylabel("time, s")
    plt.title(f"Hulk vs Loki ({tag})")
    plt.legend()
    plt.grid(True, which="both", ls=":")
    plt.tight_layout()
    plt.savefig(f"p3_{tag}.png", dpi=150)
    plt.close()
    print(f"Готово: p3_{tag}.png")


