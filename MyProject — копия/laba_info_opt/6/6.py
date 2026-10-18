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

d = read_csv("6_pic/p6_battle.csv")
n = d["n"]

# ---------- 1. Обычный масштаб ----------
plt.figure(figsize=(9, 5.5))
plt.plot(n, d["gen"],      'r-o', markersize=3, label="generation")
plt.plot(n, d["forward"],  'g-s', markersize=3, label="forward pass")
plt.plot(n, d["backward"], 'b-^', markersize=3, label="backward pass")

# output обрывается на 20000 — фильтруем
mask = d["output"] > 0
plt.plot(n[mask], d["output"][mask], 'k-d', markersize=3, label="output to file")

plt.xlabel("N")
plt.ylabel("time, s")
plt.title("Auxiliary blocks — time vs N")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("p6_battle.png", dpi=150)
plt.close()

# ---------- 2. log-log (лучше видно поведение) ----------
plt.figure(figsize=(9, 5.5))
plt.loglog(n, d["gen"],      'r-o', markersize=3, label="generation")
plt.loglog(n, d["forward"],  'g-s', markersize=3, label="forward pass")
plt.loglog(n, d["backward"], 'b-^', markersize=3, label="backward pass")
plt.loglog(n[mask], d["output"][mask], 'k-d', markersize=3, label="output to file")

# эталон ~N (линейная зависимость)
ref = n * d["forward"][0] / n[0]
plt.loglog(n, ref, 'k--', linewidth=1, label="~N")

plt.xlabel("log N")
plt.ylabel("log t")
plt.title("Auxiliary blocks — log-log")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.tight_layout()
plt.savefig("p6_battle_loglog.png", dpi=150)
plt.close()

print("Готово: p6_battle.png, p6_battle_loglog.png")