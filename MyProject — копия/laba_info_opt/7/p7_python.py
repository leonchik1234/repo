# p7_small.py
# Пункт 7: шесть сортировок на Python на N от 3 до 100, с усреднением.

import time
import random
import csv

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

def quick_sort(a):
    if len(a) <= 1:
        return a
    pivot = a[len(a) // 2]
    left  = [x for x in a if x < pivot]
    mid   = [x for x in a if x == pivot]
    right = [x for x in a if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

# heap и merge на Python — можно через встроенные средства, но для чистоты
# сделаем тоже вручную
import heapq
def heap_sort(a):
    heapq.heapify(a)
    return [heapq.heappop(a) for _ in range(len(a))]

def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    L = merge_sort(a[:m])
    R = merge_sort(a[m:])
    out = []
    i = j = 0
    while i < len(L) and j < len(R):
        if L[i] <= R[j]:
            out.append(L[i]); i += 1
        else:
            out.append(R[j]); j += 1
    out.extend(L[i:]); out.extend(R[j:])
    return out

random.seed(42)

REPS = 500   # Python медленнее, 500 повторов хватит

fns = {
    "bubble":    bubble_sort,
    "insertion": insertion_sort,
    "selection": selection_sort,
    "quick":     quick_sort,
    "heap":      heap_sort,
    "merge":     merge_sort,
}

with open("7_pic/p7_small_py.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["n"] + list(fns.keys()))

    for n in range(3, 101):
        base = [random.randint(-100000, 100000) for _ in range(n)]

        row = [n]
        for name, fn in fns.items():
            total = 0.0
            for _ in range(REPS):
                a = base.copy()
                t = time.perf_counter()
                fn(a)
                total += time.perf_counter() - t
            row.append(total / REPS)

        w.writerow(row)
        if n % 10 == 0:
            print(n, "done")