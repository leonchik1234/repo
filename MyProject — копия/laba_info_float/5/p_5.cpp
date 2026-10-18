#include <iostream>
#include <iomanip>
using namespace std;

int main() {
    cout << fixed << setprecision(2);

    float f = 0.0f;
    unsigned long long steps = 0;

    cout << "шаг\t\tf\t\tразница\t\tстатус\n";
    cout << "--------------------------------------------------------------------\n";

    while (true) {
        float prev = f;
        f += 1.0f;
        steps++;

        // Показываем только "интересные" шаги, иначе 16 млн строк
        if (steps <= 5 ||
            (f >= 16777210.0f && f <= 16777216.0f) ||
            f == prev) {

            cout << steps << "\t\t" << f << "\t\t" << (f - prev) << "\t\t";
            if (f == prev) cout << "<<< ПОЛОМКА!";
            else           cout << "растёт";
            cout << "\n";
        }

        if (f == prev) break;   // поломка — выходим
    }

    cout << "\nИтого шагов:  " << steps << "\n";
    cout << "Значение f:   " << f << "\n";
    cout << "Это 2^24 =    " << 16777216 << "\n";

    return 0;
}