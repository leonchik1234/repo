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

# стили: (цвет, тип линии, подпись)
styles = {
    "none": ("black",  "--", "no flags"),
    "O0":   ("red",    "-",  "-O0"),
    "O1":   ("orange", "-",  "-O1"),
    "O2":   ("green",  "-",  "-O2"),
    "O3":   ("blue",   "-",  "-O3"),
}

# ---------- График 1: обычный масштаб ----------
plt.figure(figsize=(9, 5.5))
for tag in ("none", "O0", "O1", "O2", "O3"):
    d = read_csv(f"p1_{tag}.csv")
    c, ls, lbl = styles[tag]
    plt.plot(d["n"], d["bubble"], color=c, linestyle=ls,
             label=lbl, linewidth=1.8)

plt.xlabel("N")
plt.ylabel("time, s")
plt.title("Bubble sort under different -O levels")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.savefig("p1_opts.png", dpi=150)
plt.close()

# ---------- График 2: log-log ----------
plt.figure(figsize=(9, 5.5))
for tag in ("none", "O0", "O1", "O2", "O3"):
    d = read_csv(f"p1_{tag}.csv")
    c, ls, lbl = styles[tag]
    plt.loglog(d["n"], d["bubble"], color=c, linestyle=ls,
               label=lbl, linewidth=1.8)

plt.xlabel("log N")
plt.ylabel("log t")
plt.title("Bubble sort under different -O levels (log-log)")
plt.legend()
plt.grid(True, which="both", ls=":")
plt.savefig("p1_opts_loglog.png", dpi=150)
plt.close()

print("Готово: p1_opts.png, p1_opts_loglog.png")