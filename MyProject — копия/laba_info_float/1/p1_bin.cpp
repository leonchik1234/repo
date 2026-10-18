#include <iostream>
using namespace std;

// Вывод 32 бит unsigned int, старшие нули включены
void print_binary(unsigned int x) {
    for (int i = 31; i >= 0; i--) {
        cout << ((x >> i) & 1);
    }
}

// Вариант с разделением по байтам — удобно для отчёта
void print_binary_pretty(unsigned int x) {
    for (int i = 31; i >= 0; i--) {
        cout << ((x >> i) & 1);
        if (i % 8 == 0 && i != 0) cout << ' ';
    }
}

int main() {
    unsigned int values[] = {0, 1, 2, 3, 255, 256, 1024, 0xDEADBEEF, 0xFFFFFFFF};

    for (unsigned int v : values) {
        cout << v << "\t\t";
        print_binary_pretty(v);
        cout << "\n";
    }
    return 0;
}