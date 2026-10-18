#include <iostream>
#include <limits>
#include <cmath>
#include <iomanip>
using namespace std;

union FloatBits {
    float f;
    unsigned int u;
};

void print_binary32(unsigned int x) {
    for (int i = 31; i >= 0; i--) {
        cout << ((x >> i) & 1);
        if (i == 31 || i == 23) cout << ' ';   // знак | степень | мантисса
    }
}

void show(const char* name, float f) {
    FloatBits fb;
    fb.f = f;

    cout << setw(8) << left << name << " = " << setw(6) << f << "  bits: ";
    print_binary32(fb.u);
    cout << "  (hex: 0x" << hex << uppercase << setw(8) << setfill('0') << fb.u
         << dec << nouppercase << setfill(' ') << ")\n";
}

int main() {

    float one  = 1.0f;
    float zero = 0.0f;

    show("+inf",  one / zero);
    show("-inf", -one / zero);
    show("nan",   zero / zero);

    return 0;
}