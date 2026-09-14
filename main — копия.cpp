#include <iostream>
using namespace std;

unsigned long long int get_a_hexadecimal() {
    unsigned long long res = 0;
    char c;
    while (cin.get(c)) {
        if (c == ' ' || c == '\n')
            break;

        int s;
        if (c >= '0' && c <= '9')
            s = c - '0';
        else if (c >= 'A' && c <= 'F')
            s = c - 'A' + 10;
        else if (c >= 'a' && c <= 'f')
            s = c - 'a' + 10;
        else 
            continue;

        res = res * 16 + s;
    }
    return res;
}
int main()
{
    cout << get_a_hexadecimal() << endl;
    return 0;
}