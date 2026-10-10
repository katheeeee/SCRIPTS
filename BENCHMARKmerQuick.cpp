#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

typedef void (*Orden)(int[], int);

double ahora(void) {
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + t.tv_nsec * 1e-9;
}

void mezclar(int a[], int aux[], int izq, int medio, int der) {
    int i = izq, j = medio + 1, k = izq;
    while (i <= medio && j <= der) {
        if (a[i] <= a[j]) aux[k++] = a[i++];
        else aux[k++] = a[j++];
    }
    while (i <= medio) aux[k++] = a[i++];
    while (j <= der) aux[k++] = a[j++];
    memcpy(a + izq, aux + izq, (der - izq + 1) * sizeof(int));
}

void merge_sort_rec(int a[], int aux[], int izq, int der) {
    if (izq >= der) return;
    int medio = izq + (der - izq) / 2;
    merge_sort_rec(a, aux, izq, medio);
    merge_sort_rec(a, aux, medio + 1, der);
    mezclar(a, aux, izq, medio, der);
}

void merge_sort(int a[], int n) {
    int *aux = (int *)malloc(n * sizeof(int));
    merge_sort_rec(a, aux, 0, n - 1);
    free(aux);
}

void intercambiar(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int particion(int a[], int bajo, int alto) {
    int pivote = a[alto];
    int i = bajo - 1;
    for (int j = bajo; j < alto; j++) {
        if (a[j] <= pivote) {
            i++;
            intercambiar(&a[i], &a[j]);
        }
    }
    intercambiar(&a[i + 1], &a[alto]);
    return i + 1;
}

void quick_sort_rec(int a[], int bajo, int alto) {
    if (bajo < alto) {
        int p = particion(a, bajo, alto);
        quick_sort_rec(a, bajo, p - 1);
        quick_sort_rec(a, p + 1, alto);
    }
}

void quick_sort(int a[], int n) {
    quick_sort_rec(a, 0, n - 1);
}

int esta_ordenado(int a[], int n) {
    for (int i = 1; i < n; i++)
        if (a[i - 1] > a[i]) return 0;
    return 1;
}

void generar(int a[], int n, int caso) {
    for (int i = 0; i < n; i++) {
        if (caso == 0) a[i] = rand();
        else if (caso == 1) a[i] = i;
        else a[i] = n - i;
    }
}

double medir(Orden f, int base[], int n, int reps) {
    int *copia = (int *)malloc(n * sizeof(int));
    double total = 0;
    for (int r = 0; r < reps; r++) {
        memcpy(copia, base, n * sizeof(int));
        double t0 = ahora();
        f(copia, n);
        total += ahora() - t0;
        if (!esta_ordenado(copia, n)) {
            fprintf(stderr, "Error: arreglo no ordenado\n");
            exit(1);
        }
    }
    free(copia);
    return total / reps;
}

int main(void) {
    const char *nombres[] = {"ALEATORIO", "ASCENDENTE (ya ordenado)", "DESCENDENTE (orden inverso)"};
    int inicio[] = {10000, 1000, 1000};
    int pasos[] = {9, 6, 6};
    FILE *csv = fopen("resultados.csv", "w");
    fprintf(csv, "caso,n,merge_s,quick_s\n");
    srand(42);

    for (int caso = 0; caso < 3; caso++) {
        printf("\n=== Caso %s ===\n", nombres[caso]);
        printf("%-9s %-12s %-12s %-14s %-14s %-12s %-8s %-8s\n",
               "n", "merge (s)", "quick (s)", "merge/(nlogn)", "quick/(nlogn)", "quick/n^2", "x_merge", "x_quick");
        double prev_m = 0, prev_q = 0;
        int n = inicio[caso];
        for (int p = 0; p < pasos[caso]; p++, n *= 2) {
            int *base = (int *)malloc(n * sizeof(int));
            generar(base, n, caso);
            int reps = 200000 / n;
            if (reps < 1) reps = 1;
            double tm = medir(merge_sort, base, n, reps);
            double tq = medir(quick_sort, base, n, reps);
            double nlogn = n * log2((double)n);
            printf("%-9d %-12.6f %-12.6f %-14.3e %-14.3e %-12.3e %-8.2f %-8.2f\n",
                   n, tm, tq, tm / nlogn, tq / nlogn, tq / ((double)n * n),
                   prev_m > 0 ? tm / prev_m : 0.0, prev_q > 0 ? tq / prev_q : 0.0);
            fprintf(csv, "%d,%d,%.9f,%.9f\n", caso, n, tm, tq);
            prev_m = tm;
            prev_q = tq;
            free(base);
        }
    }
    fclose(csv);
    return 0;
}
