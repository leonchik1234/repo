#include <iostream>
using namespace std;

int main() {
    int F, N, M, D;
    cin >> F >> N >> M >> D;
    
    int expected[100], real[100];
    for (int i = 0; i < N; i++) cin >> expected[i];
    for (int i = 0; i < N; i++) cin >> real[i];
    
    int c = 0;
    
    for (int i = 0; i < N; i++) {
        if (F <= 0) break;
        F -= real[i];
        
        if (real[i] < expected[i]) {
            F += M;
        } else if (real[i] > expected[i]) {
            F -= D;
        }
        
        c++;
    }
    
    cout << c << endl;
    return 0;
}