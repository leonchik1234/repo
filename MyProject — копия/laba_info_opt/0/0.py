import csv
import numpy as np
import matplotlib.pyplot as plt

def read_csv(path):
    with open(path) as f:
        reader = csv.reader(f)
        header = next(reader)
        data = {h: [] for h in header}
        for row in reader:
            for h, v in zip(header, row):
                try: data[h].append(float(v))
                except ValueError: data[h].append(v)
        return {k: np.array(v) for k, v in data.items()}

d = read_csv("p0_slow.csv")
n = d["n"]

# --- Обычный масштаб ---
plt.figure(figsize=(8, 5))
for key in ("bubble", "insertion", "selection"):
    plt.plot(n, d[key], label=key)
plt.xlabel("N")
plt.ylabel("time, s")
plt.title("O(N^2) sorts")
plt.legend()
plt.grid(True)
plt.savefig("p0_linear.png", dpi=150)
plt.close()

# --- Двойной логарифмический ---
plt.figure(figsize=(8, 5))
for key in ("bubble", "insertion", "selection"):
    plt.loglog(n, d[key], label=key)

ref = n**2 * d["bubble"][0] / n[0]**2
plt.loglog(n, ref, 'k--', label="~N^2")

plt.xlabel("log N")
plt.ylabel("log t")
plt.title("O(N^2) sorts, log-log")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.savefig("p0_loglog.png", dpi=150)
plt.close()

print("Готово: p0_linear.png, p0_loglog.png")