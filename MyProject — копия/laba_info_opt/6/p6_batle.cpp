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

const int MAXN = 500001;
int a[MAXN];

int main() {
    std::ofstream f("p6_battle.csv");
    f << "n,gen,forward,backward,output\n";

    std::ofstream devnull("p6_devnull.txt");

    for (int n = 1000; n <= 500000; n = n * 11 / 10) {

        // ---- 1. генерация массива ----
        double t_gen;
        {
            double t = get_time();
            for (int i = 0; i < n; ++i) a[i] = rand_uns(-100000, 100000);
            t_gen = get_time() - t;
        }

        // ---- 2. прямой проход с арифметикой ----
        double t_fwd;
        {
            volatile long long s = 0;
            double t = get_time();
            for (int i = 0; i < n; ++i) s += a[i] * 3 + 1;
            t_fwd = get_time() - t;
            (void)s;
        }

        // ---- 3. обратный проход с арифметикой ----
        double t_bwd;
        {
            volatile long long s = 0;
            double t = get_time();
            for (int i = n - 1; i >= 0; --i) s += a[i] * 3 + 1;
            t_bwd = get_time() - t;
            (void)s;
        }

        // ---- 4. вывод массива ----
        double t_out = 0;
        if (n <= 20000) {
            double t = get_time();
            for (int i = 0; i < n; ++i) devnull << a[i] << ' ';
            devnull << '\n';
            t_out = get_time() - t;
        }

        f << n << "," << t_gen << "," << t_fwd << ","
          << t_bwd << "," << t_out << "\n";

        std::cout << n << " done" << std::endl;
    }

    devnull.close();
    f.close();
    return 0;
}