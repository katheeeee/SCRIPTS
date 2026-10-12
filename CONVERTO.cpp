#include <iostream>
#include <string>
#include <cctype>
#include <algorithm>
#include <limits>

using namespace std;

void limpiarBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

bool esValido(const string& num, int base) {
    if (num.empty()) return false;
    for (char c : num) {
        char up = toupper(c);
        int valor;
        if (up >= '0' && up <= '9') valor = up - '0';
        else if (up >= 'A' && up <= 'F') valor = up - 'A' + 10;
        else return false;
        if (valor >= base) return false;
    }
    return true;
}

bool desborda(const string& num, int base) {
    long long resultado = 0;
    long long maximo = numeric_limits<long long>::max();
    for (char c : num) {
        char up = toupper(c);
        int valor;
        if (up >= '0' && up <= '9') valor = up - '0';
        else valor = up - 'A' + 10;
        if (resultado > (maximo - valor) / base) return true;
        resultado = resultado * base + valor;
    }
    return false;
}

long long aDecimal(const string& num, int base) {
    long long resultado = 0;
    for (char c : num) {
        char up = toupper(c);
        int valor;
        if (up >= '0' && up <= '9') valor = up - '0';
        else valor = up - 'A' + 10;
        resultado = resultado * base + valor;
    }
    return resultado;
}

string desdeDecimal(long long num, int base) {
    if (num == 0) return "0";
    string resultado = "";
    string digitos = "0123456789ABCDEF";
    bool negativo = num < 0;
    if (negativo) num = -num;
    while (num > 0) {
        resultado = digitos[num % base] + resultado;
        num /= base;
    }
    if (negativo) resultado = "-" + resultado;
    return resultado;
}

string nombreBase(int base) {
    switch (base) {
        case 2: return "binario";
        case 8: return "octal";
        case 10: return "decimal";
        case 16: return "hexadecimal";
    }
    return "";
}

int pedirBase(const string& etiqueta) {
    int base;
    while (true) {
        cout << "Seleccione la base " << etiqueta << ":\n";
        cout << "1. Binario\n2. Octal\n3. Decimal\n4. Hexadecimal\n";
        cout << "Opcion: ";
        cin >> base;
        if (cin.fail()) {
            limpiarBuffer();
            cout << "ADVERTENCIA: entrada invalida. Intente de nuevo.\n";
            continue;
        }
        limpiarBuffer();
        if (base == 1) return 2;
        if (base == 2) return 8;
        if (base == 3) return 10;
        if (base == 4) return 16;
        cout << "ADVERTENCIA: opcion invalida. Intente de nuevo.\n";
    }
}

string pedirNumero(int base) {
    string num;
    while (true) {
        cout << "Ingrese el numero en " << nombreBase(base) << ": ";
        cin >> num;
        limpiarBuffer();
        transform(num.begin(), num.end(), num.begin(), ::toupper);
        if (!esValido(num, base)) {
            cout << "ADVERTENCIA: numero invalido para base " << nombreBase(base) << ". Intente de nuevo.\n";
            continue;
        }
        if (desborda(num, base)) {
            cout << "ADVERTENCIA: numero demasiado grande, no se puede representar (maximo 9223372036854775807 en decimal). Intente de nuevo.\n";
            continue;
        }
        return num;
    }
}

char pedirSN() {
    string respuesta;
    while (true) {
        cout << "\nDesea realizar otra conversion? (S/N): ";
        cin >> respuesta;
        limpiarBuffer();
        if (respuesta.empty()) continue;
        char c = toupper(respuesta[0]);
        if (c == 'S' || c == 'N') return c;
        cout << "ADVERTENCIA: respuesta invalida, escriba S o N.\n";
    }
}

int main() {
    char repetir = 'S';
    while (repetir == 'S') {
        int baseOrigen = pedirBase("de origen");
        string num = pedirNumero(baseOrigen);
        long long decimal = aDecimal(num, baseOrigen);

        int baseDestino = pedirBase("de destino");
        string resultado = desdeDecimal(decimal, baseDestino);

        cout << "\n" << num << " en " << nombreBase(baseOrigen) << " equivale a "
             << resultado << " en " << nombreBase(baseDestino) << "\n";

        repetir = pedirSN();
    }

    cout << "Programa finalizado." << endl;
    return 0;
}