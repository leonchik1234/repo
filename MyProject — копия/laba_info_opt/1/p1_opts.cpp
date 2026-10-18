#include <fstream>
#include <iostream>
#include <chrono>
#include <random>

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

void my_swap(int& a, int& b) { int t = a; a = b; b = t; }

void bubble_sort(int* a, int n) {
    for (int i = 0; i < n - 1; ++i)
        for (int j = 0; j < n - 1 - i; ++j)
            if (a[j] > a[j + 1]) my_swap(a[j], a[j + 1]);
}

void copy_array(int* d, int* s, int n) { for (int i = 0; i < n; ++i) d[i] = s[i]; }

int base[30001], work[30001];

int main(int argc, char** argv) {
    const char* tag = (argc > 1) ? argv[1] : "O0";

    // имя файла собираем вручную (string запрещён)
    char fname[64] = "p1_";
    int i = 3;
    for (int k = 0; tag[k] != 0 && i < 60; ++k) fname[i++] = tag[k];
    fname[i++] = '.'; fname[i++] = 'c'; fname[i++] = 's'; fname[i++] = 'v';
    fname[i] = 0;

    std::ofstream f(fname);
    f << "n,bubble\n";

    // логарифмическая сетка: ~50 точек от 100 до 20000
    for (int n = 100; n <= 20000; n = n * 11 / 10) {
        for (int k = 0; k < n; ++k) base[k] = rand_uns(-100000, 100000);
        copy_array(work, base, n);

        double t = get_time();
        bubble_sort(work, n);
        t = get_time() - t;

        f << n << "," << t << "\n";

        // защита от вырезания оптимизатором -O3
        volatile int sink = work[0];
        (void)sink;

        std::cout << n << " done" << std::endl;
    }

    f.close();
    return 0;
}