#include <fstream>
#include <iostream>
#include <chrono>
#include <random>

double get_time() {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(
        std::chrono::steady_clock::now().time_since_epoch()).count() / 1e9;
}

int rand_uns(int min, int max) {
    unsigned seed = std::chrono::steady_clock::now().time_since_epoch().count();
    static std::default_random_engine e(seed);
    std::uniform_int_distribution<int> d(min, max);
    return d(e);
}

void my_swap(int& a, int& b) { int t = a; a = b; b = t; }
void copy_array(int* d, const int* s, int n) { for (int i = 0; i < n; ++i) d[i] = s[i]; }

// ==================== O(N^2) ====================

void bubble_sort(int* a, int n) {
    for (int i = 0; i < n - 1; ++i)
        for (int j = 0; j < n - 1 - i; ++j)
            if (a[j] > a[j + 1]) my_swap(a[j], a[j + 1]);
}
void insertion_sort(int* a, int n) {
    for (int i = 1; i < n; ++i) {
        int key = a[i], j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; --j; }
        a[j + 1] = key;
    }
}
void selection_sort(int* a, int n) {
    for (int i = 0; i < n - 1; ++i) {
        int m = i;
        for (int j = i + 1; j < n; ++j) if (a[j] < a[m]) m = j;
        if (m != i) my_swap(a[i], a[m]);
    }
}

// ==================== O(N log N) ====================

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
void quick_sort(int* a, int n) { if (n > 0) quick_sort_rec(a, 0, n - 1); }

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
    static int buf[101];
    merge_sort_rec(a, buf, 0, n - 1);
}

// ==================== MAIN ====================

const int MAXN = 101;
int base[MAXN], work[MAXN];

int main() {
    std::ofstream f("p7_small.csv");
    f << "n,bubble,insertion,selection,quick,heap,merge\n";

    const int REPS = 5000;   // усреднение, чтобы шум таймера не портил график

    for (int n = 3; n <= 100; ++n) {
        double sum[6] = {0,0,0,0,0,0};

        for (int rep = 0; rep < REPS; ++rep) {
            for (int k = 0; k < n; ++k) base[k] = rand_uns(-100000, 100000);

            double t;

            copy_array(work, base, n); t = get_time(); bubble_sort(work, n);    sum[0] += get_time() - t;
            copy_array(work, base, n); t = get_time(); insertion_sort(work, n); sum[1] += get_time() - t;
            copy_array(work, base, n); t = get_time(); selection_sort(work, n); sum[2] += get_time() - t;
            copy_array(work, base, n); t = get_time(); quick_sort(work, n);     sum[3] += get_time() - t;
            copy_array(work, base, n); t = get_time(); heap_sort(work, n);      sum[4] += get_time() - t;
            copy_array(work, base, n); t = get_time(); merge_sort(work, n);     sum[5] += get_time() - t;
        }

        f << n;
        for (int q = 0; q < 6; ++q) f << "," << sum[q] / REPS;
        f << "\n";
        std::cout << n << " done" << std::endl;
    }

    f.close();
    return 0;
}