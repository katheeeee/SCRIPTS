#include <iostream>
using namespace std;

int main() {
    const int N = 10000;
    const int B = 100;

    float total = 0;
    for (int g = 0; g < N / B; g++) {
        float grupo = 0;
        for (int j = 0; j < B; j++) {
            grupo = grupo + 0.00001f;
        }
        total = total + grupo;
    }
    float suma = 1 + total;

    cout << "Resultado: " << suma << endl;

    return 0;
}