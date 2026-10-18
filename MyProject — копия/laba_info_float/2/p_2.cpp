#include <iostream>
#include <iomanip>
#include <cmath>
using namespace std;

// ---------- из пункта 1 ----------
void print_binary(unsigned int x) {
    for (int i = 31; i >= 0; i--) {
        cout << ((x >> i) & 1);
        if (i == 31 || i == 23) cout << ' ';   // знак | степень | мантисса
    }
}

// ---------- union: одни и те же байты, два взгляда ----------
union FloatBits {
    float f;
    unsigned int u;
};

void analyze(float value) {
    FloatBits fb;
    fb.f = value;

    unsigned int sign = (fb.u >> 31) & 0x1;
    unsigned int exp  = (fb.u >> 23) & 0xFF;
    unsigned int mant =  fb.u        & 0x7FFFFF;

    cout << "Число:      " << value << "\n";
    cout << "Биты:       ";
    print_binary(fb.u);
    cout << "\n";
    cout << "  знак:     " << sign << "\n";
    cout << "  степень:  " << exp << "  (смещение 127 -> " << (int)exp - 127 << ")\n";
    cout << "  мантисса: 0x" << hex << mant << dec
         << "  (" << mant << ")\n";

    // Восстановление значения вручную (для нормализованных)
    if (exp != 0 && exp != 255) {
        double reconstructed = (1.0 + mant / 8388608.0)   // 2^23
                             * pow(2.0, (int)exp - 127)
                             * (sign ? -1 : 1);
        cout << "  собрано:  " << setprecision(10) << reconstructed << "\n";
    }
    cout << "----------------------------------------\n";
}

int main() {
    cout << fixed << setprecision(6);

    analyze(1.0f);
    analyze(-2.5f);
    analyze(0.1f);
    analyze(3.14159f);
    analyze(0.0f);

    return 0;
}