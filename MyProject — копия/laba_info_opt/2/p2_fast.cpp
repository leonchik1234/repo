#include <fstream>
#include <iostream>
#include <chrono>
#include <random>

//======================БАЗА=============================
double get_time() {
    return std::chrono::duration_cast<std::chrono::microseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count() / 1e6;
}

int rand_uns(int min, int max) {
    unsigned seed = std::chrono::steady_clock::now().time_since_epoch().count();
    static std::default_random_engine e(seed);
    std::uniform_int_distribution<int> d(min, max);
    return d(e);
}

void my_swap(int& a, int& b) {
    int tmp = a;
    a = b;
    b = tmp;
}

void copy_array(int* d, const int* s, int n) { for (int i = 0; i < n; ++i) d[i] = s[i]; }

// ==================== БЫСТРАЯ (Хоар) ====================

void quick_sort_rec(int* a, int l, int r) {
    int i = l, j = r;
    int pivot = a[(l + r) / 2];
    while (i <= j) {
        while (a[i] < pivot) ++i;
        while (a[j] > pivot) --j;
        if (i <= j) { my_swap(a[i], a[j]); ++i; --j; }
    }
    if (l < j) quick_sort_rec(a, l, j);
    if (i < r) quick_sort_rec(a, i, r);
}

void quick_sort(int* a, int n) {
    if (n > 0) quick_sort_rec(a, 0, n - 1);
}

// ==================== СЛИЯНИЕМ ====================

void merge_sort_rec(int* a, int* buf, int l, int r) {
    if (l >= r) return;
    int m = (l + r) / 2;
    merge_sort_rec(a, buf, l, m);
    merge_sort_rec(a, buf, m + 1, r);

    int i = l, j = m + 1, k = l;
    while (i <= m && j <= r) buf[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
    while (i <= m) buf[k++] = a[i++];
    while (j <= r) buf[k++] = a[j++];
    for (int t = l; t <= r; ++t) a[t] = buf[t];
}

void merge_sort(int* a, int n) {
    if (n <= 1) return;
    static int buf[500001];   // хватает до N = 500000
    merge_sort_rec(a, buf, 0, n - 1);
}

// ==================== ПИРАМИДАЛЬНАЯ ====================

void sift_down(int* a, int start, int end) {
    int root = start;
    while (2 * root + 1 <= end) {
        int child = 2 * root + 1;
        if (child + 1 <= end && a[child] < a[child + 1]) ++child;
        if (a[root] < a[child]) { my_swap(a[root], a[child]); root = child; }
        else return;
    }
}

void heap_sort(int* a, int n) {
    for (int i = n / 2 - 1; i >= 0; --i) sift_down(a, i, n - 1);
    for (int i = n - 1; i > 0; --i) {
        my_swap(a[0], a[i]);
        sift_down(a, 0, i - 1);
    }
}

// ==================== MAIN ====================

const int MAXN = 500001;
int base[MAXN], work[MAXN];

int main() {
    std::ofstream f("p2_fast.csv");
    f << "n,quick,heap,merge\n";

    // логарифмическая сетка: ~60 точек от 100 до 500000
    for (int n = 100; n <= 500000; n = n * 11 / 10) {
        for (int i = 0; i < n; ++i) base[i] = rand_uns(-100000, 100000);

        double t1, t2, t3;

        copy_array(work, base, n); t1 = get_time(); quick_sort(work, n); t1 = get_time() - t1;
        copy_array(work, base, n); t2 = get_time(); heap_sort(work, n);  t2 = get_time() - t2;
        copy_array(work, base, n); t3 = get_time(); merge_sort(work, n); t3 = get_time() - t3;

        f << n << "," << t1 << "," << t2 << "," << t3 << "\n";

        // защита от вырезания оптимизатором
        volatile int sink = work[0];
        (void)sink;

        std::cout << n << " done" << std::endl;
    }

    f.close();
    return 0;

}