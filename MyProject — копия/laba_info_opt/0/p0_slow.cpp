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

//=====================СОРТИРОВКИ=========================

//пузырек
void bubble_sort(int* a, int n){
    for(int i = 0; i < n; i++){
        for(int j = 0; j < n - i - 1; j++){
            if (a[j] > a[j + 1]) my_swap(a[j], a[j + 1]);
        }
    }
}

//вставка
void insertion_sort(int* a, int n){
    for (int i = 1; i < n; ++i) {
        int key = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > key) {
            a[j + 1] = a[j];
            --j;
        }
        a[j + 1] = key;
    }
}

//простой выбор
void selection_sort(int* a, int n) {
    for (int i = 0; i < n - 1; ++i) {
        int m = i;
        for (int j = i + 1; j < n; ++j)
            if (a[j] < a[m]) m = j;
        if (m != i) my_swap(a[i], a[m]);
    }
}

//====================MAIN=======================

int base[30001];
int work[30001];

void copy_array(int* dst, const int* src, int n) {
    for (int i = 0; i < n; ++i) dst[i] = src[i];
}

int main(){
    std::ofstream f("p0_slow.csv");
    f << "n,bubble,insertion,selection\n";

    for (int n = 100; n <= 10000; n += 100) {

        // генерация случайного массива
        for (int i = 0; i < n; ++i) base[i] = rand_uns(-100000, 100000);

        double t1, t2, t3;

        // --- пузырёк ---
        copy_array(work, base, n);
        t1 = get_time();
        bubble_sort(work, n);
        t1 = get_time() - t1;

        // --- вставка ---
        copy_array(work, base, n);
        t2 = get_time();
        insertion_sort(work, n);
        t2 = get_time() - t2;

        // --- выбор ---
        copy_array(work, base, n);
        t3 = get_time();
        selection_sort(work, n);
        t3 = get_time() - t3;

        f << n << "," << t1 << "," << t2 << "," << t3 << "\n";
        std::cout << n << " done" << std::endl;
    }

    f.close();
    return 0;

}