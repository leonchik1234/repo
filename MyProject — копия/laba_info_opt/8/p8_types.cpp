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

// ==================== СТРУКТУРЫ ====================

struct Light {
    int a;
    int b;
};

struct Heavy {
    int    a, b, c, d;
    double x, y, z;
    char   buf[128];
};

// операторы сравнения — по одному ключевому полю
bool operator<(const Light& l, const Light& r) { return l.a < r.a; }
bool operator>(const Light& l, const Light& r) { return l.a > r.a; }
bool operator<=(const Light& l, const Light& r) { return l.a <= r.a; }
bool operator==(const Light& l, const Light& r) { return l.a == r.a; }

bool operator<(const Heavy& l, const Heavy& r) { return l.a < r.a; }
bool operator>(const Heavy& l, const Heavy& r) { return l.a > r.a; }
bool operator<=(const Heavy& l, const Heavy& r) { return l.a <= r.a; }
bool operator==(const Heavy& l, const Heavy& r) { return l.a == r.a; }

// ==================== ШАБЛОННЫЕ СОРТИРОВКИ ====================

template <typename T>
void my_swap(T& a, T& b) { T t = a; a = b; b = t; }

template <typename T>
void insertion_sort(T* a, int n) {
    for (int i = 1; i < n; ++i) {
        T key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) { a[j + 1] = a[j]; --j; }
        a[j + 1] = key;
    }
}

template <typename T>
void quick_sort_rec(T* a, int l, int r) {
    int i = l, j = r;
    T pivot = a[(l + r) / 2];
    while (i <= j) {
        while (a[i] < pivot) ++i;
        while (a[j] > pivot) --j;
        if (i <= j) { my_swap(a[i], a[j]); ++i; --j; }
    }
    if (l < j) quick_sort_rec(a, l, j);
    if (i < r) quick_sort_rec(a, i, r);
}
template <typename T>
void quick_sort(T* a, int n) { if (n > 0) quick_sort_rec(a, 0, n - 1); }

// ==================== БУФЕРЫ ====================

const int MAXN = 500001;

char      buf_char[MAXN];
short     buf_short[MAXN];
int       buf_int[MAXN];
long      buf_long[MAXN];
long long buf_longlong[MAXN];
Light     buf_light[MAXN];
Heavy     buf_heavy[MAXN];

// ==================== ЗАМЕР ОДНОГО ТИПА ====================

template <typename T>
void bench(std::ofstream& f, const char* name, int n) {
    for (int i = 0; i < n; ++i) buf_int[i] = rand_uns(0, 1000000);

}

// ==================== MAIN ====================

int main() {
    std::ofstream f("p8_types.csv");
    f << "n,type,time\n";

    for (int n = 1000; n <= 500000; n = n * 12 / 10) {

        // ---------- char ----------
        {
            for (int i = 0; i < n; ++i) buf_char[i] = (char)rand_uns(0, 127);
            double t = get_time();
            quick_sort(buf_char, n);
            t = get_time() - t;
            f << n << ",char," << t << "\n";
            volatile char sink = buf_char[0]; (void)sink;
        }

        // ---------- short ----------
        {
            for (int i = 0; i < n; ++i) buf_short[i] = (short)rand_uns(0, 32000);
            double t = get_time();
            quick_sort(buf_short, n);
            t = get_time() - t;
            f << n << ",short," << t << "\n";
            volatile short sink = buf_short[0]; (void)sink;
        }

        // ---------- int ----------
        {
            for (int i = 0; i < n; ++i) buf_int[i] = rand_uns(0, 1000000);
            double t = get_time();
            quick_sort(buf_int, n);
            t = get_time() - t;
            f << n << ",int," << t << "\n";
            volatile int sink = buf_int[0]; (void)sink;
        }

        // ---------- long ----------
        {
            for (int i = 0; i < n; ++i) buf_long[i] = rand_uns(0, 1000000);
            double t = get_time();
            quick_sort(buf_long, n);
            t = get_time() - t;
            f << n << ",long," << t << "\n";
            volatile long sink = buf_long[0]; (void)sink;
        }

        // ---------- long long ----------
        {
            for (int i = 0; i < n; ++i) buf_longlong[i] = rand_uns(0, 1000000);
            double t = get_time();
            quick_sort(buf_longlong, n);
            t = get_time() - t;
            f << n << ",longlong," << t << "\n";
            volatile long long sink = buf_longlong[0]; (void)sink;
        }

        // ---------- Light (8 байт) ----------
        {
            for (int i = 0; i < n; ++i) {
                buf_light[i].a = rand_uns(0, 1000000);
                buf_light[i].b = i;
            }
            double t = get_time();
            quick_sort(buf_light, n);
            t = get_time() - t;
            f << n << ",Light," << t << "\n";
            volatile int sink = buf_light[0].a; (void)sink;
        }

        // ---------- Heavy (256+ байт) ----------
        {
            for (int i = 0; i < n; ++i) {
                buf_heavy[i].a = rand_uns(0, 1000000);
                buf_heavy[i].b = i;
                buf_heavy[i].c = i * 2;
                buf_heavy[i].d = i * 3;
                buf_heavy[i].x = i * 0.1;
                buf_heavy[i].y = i * 0.2;
                buf_heavy[i].z = i * 0.3;
                for (int k = 0; k < 128; ++k) buf_heavy[i].buf[k] = (char)k;
            }
            double t = get_time();
            quick_sort(buf_heavy, n);
            t = get_time() - t;
            f << n << ",Heavy," << t << "\n";
            volatile int sink = buf_heavy[0].a; (void)sink;
        }

        std::cout << n << " done" << std::endl;
    }

    f.close();
    return 0;
}