#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

// ---------- из пункта 0 ----------
unsigned long long int my_pow(unsigned long long int x, unsigned long long int n) {
    unsigned long long int result = 1;
    for (unsigned long long int i = 0; i < n; i++) result *= x;
    return result;
}

// ---------- из пункта 1/2 ----------
union FloatBits {
    float f;
    unsigned int u;
};

union DoubleBits {
    double d;
    unsigned long long u;
};

// 32 бита с разделителями: знак | степень | мантисса
void print_binary32(unsigned int x) {
    for (int i = 31; i >= 0; i--) {
        cout << ((x >> i) & 1);
        if (i == 31 || i == 23) cout << ' ';
    }
}

// 64 бита с разделителями: знак | степень | мантисса
void print_binary64(unsigned long long x) {
    for (int i = 63; i >= 0; i--) {
        cout << ((x >> i) & 1);
        if (i == 63 || i == 52) cout << ' ';
    }
}

int main() {
    cout << fixed;
    cout.precision(2);

    const unsigned long long int BASE = 3;

    // ========== FLOAT ==========
    cout << "========== FLOAT (base = 3) ==========\n";
    cout << "n\tmy_pow\t\t\tstd::pow(float)\t\tbits\n";
    cout << "--------------------------------------------------------------------------\n";

    for (unsigned long long int i = 0; i < 25; i++) {
        unsigned long long int exact = my_pow(BASE, i);
        FloatBits fb;
        fb.f = pow((float)BASE, (float)i);

        cout << i << "\t" << exact << "\t\t\t" << fb.f << "\t\t";
        print_binary32(fb.u);
        cout << "\n";
    }

    // ========== DOUBLE ==========
    cout << "\n========== DOUBLE (base = 3) ==========\n";
    cout << "n\tmy_pow\t\t\t\tstd::pow(double)\tbits\n";
    cout << "--------------------------------------------------------------------------------------------\n";

    for (unsigned long long int i = 0; i < 40; i++) {
        unsigned long long int exact = my_pow(BASE, i);
        DoubleBits db;
        db.d = pow((double)BASE, (double)i);

        cout << i << "\t" << exact << "\t\t\t\t" << db.d << "\t\t";
        print_binary64(db.u);
        cout << "\n";
    }

    return 0;
}