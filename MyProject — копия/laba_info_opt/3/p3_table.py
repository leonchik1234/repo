import csv

def read_csv(path):
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        data = {h: [] for h in header}
        for row in r:
            for h, v in zip(header, row):
                data[h].append(float(v))
        return data

algos = ["bubble", "insertion", "selection", "quick", "heap", "merge"]
tags = ["O0", "O1", "O2", "O3"]

# средние времена (без учёта -1 заглушек)
avg = {}
for tag in tags:
    d = read_csv(f"p3_{tag}.csv")
    avg[tag] = {}
    for algo in algos:
        vals = [v for v in d[algo] if v >= 0]
        avg[tag][algo] = sum(vals) / len(vals) if vals else 0

print(f"{'algo':<12}", end="")
for tag in tags:
    print(f"{tag:>10}", end="")
print()

for algo in algos:
    print(f"{algo:<12}", end="")
    base = avg["O0"][algo]
    for tag in tags:
        sp = base / avg[tag][algo] if avg[tag][algo] > 0 else 0
        print(f"{sp:>9.2f}x", end="")
    print()