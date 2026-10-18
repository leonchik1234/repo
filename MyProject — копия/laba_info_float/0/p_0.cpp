#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;

unsigned long long int my_pow(unsigned long long int x, unsigned long long int n) {
    unsigned long long int result = 1;
    for (unsigned long long int i = 0; i < n; i++) {
        result *= x;
    }
    return result;
}

int main() {
    cout << fixed;
    cout.precision(2);
    
    unsigned long long int base = 3;
    
    cout << "n\tmy_pow\t\tstd::pow(float)\tstd::pow(double)\n";
    cout << "----------------------------------------------------------\n";
    
    for (unsigned long long int i = 0; i < 41; i++) {
        unsigned long long int mine = my_pow(base, i);
        float f = pow((float)base, (float)i);
        double d = pow((double)base, (double)i);
        
        cout << i << "\t" << mine << "\t\t" << f << "\t\t" << d << "\n";
    }
    return 0;
}