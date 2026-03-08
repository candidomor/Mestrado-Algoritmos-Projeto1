#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
#include <fstream>
#include <string>
#include <cmath>
#include <iomanip>

using namespace std;
using namespace std::chrono;

void bubbleSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        bool swapped = false;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j+1]) {
                swap(arr[j], arr[j+1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void selectionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 0; i < n; i++) {
        int min_idx = i;
        for (int j = i+1; j < n; j++) {
            if (arr[min_idx] > arr[j]) {
                min_idx = j;
            }
        }
        swap(arr[i], arr[min_idx]);
    }
}

void insertionSort(vector<int>& arr) {
    int n = arr.size();
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

void merge(vector<int>& arr, vector<int>& temp, int left, int mid, int right) {
    int i = left;
    int j = mid + 1;
    int k = left;

    while (i <= mid && j <= right) {
        if (arr[i] <= arr[j]) {
            temp[k++] = arr[i++];
        } else {
            temp[k++] = arr[j++];
        }
    }

    while (i <= mid) {
        temp[k++] = arr[i++];
    }
    while (j <= right) {
        temp[k++] = arr[j++];
    }

    for (int x = left; x <= right; x++) {
        arr[x] = temp[x];
    }
}

void mergeSortRecursive(vector<int>& arr, vector<int>& temp, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSortRecursive(arr, temp, left, mid);
        mergeSortRecursive(arr, temp, mid + 1, right);
        merge(arr, temp, left, mid, right);
    }
}

void mergeSort(vector<int>& arr) {
    vector<int> temp(arr.size());
    mergeSortRecursive(arr, temp, 0, arr.size() - 1);
}

int partition(vector<int>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    swap(arr[mid], arr[high]);

    int pivot = arr[high];
    int i = (low - 1);
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSortRecursive(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSortRecursive(arr, low, pi - 1);
        quickSortRecursive(arr, pi + 1, high);
    }
}

void quickSort(vector<int>& arr) {
    quickSortRecursive(arr, 0, arr.size() - 1);
}

vector<int> generateRandomArray(int size, mt19937& gen) {
    vector<int> arr(size);
    uniform_int_distribution<> distrib(0, size * 2);
    for (int i = 0; i < size; i++) {
        arr[i] = distrib(gen);
    }
    return arr;
}

vector<int> generateSortedArray(int size) {
    vector<int> arr(size);
    for (int i = 0; i < size; i++) {
        arr[i] = i;
    }
    return arr;
}

vector<int> generateReverseSortedArray(int size) {
    vector<int> arr(size);
    for (int i = 0; i < size; i++) {
        arr[i] = size - i;
    }
    return arr;
}

int main() {
    vector<int> tamanhos = { 1000, 10000, 100000 };
    int K_AMOSTRAS = 5;
    vector<string> tipos = { "Aleatório", "Crescente", "Decrescente" };
    vector<string> nomes_algoritmos = { "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort" };

    typedef void (*SortFunction)(vector<int>&);
    vector<SortFunction> algoritmos = { bubbleSort, selectionSort, insertionSort, mergeSort, quickSort };

    mt19937 gen(42);

    cout << "Iniciando bateria de testes C++ nativo (" << K_AMOSTRAS << " amostras).\n";

    string jsonOutput = "{\n";

    for (size_t a = 0; a < algoritmos.size(); a++) {
        jsonOutput += "  \"" + nomes_algoritmos[a] + "\": {\n";
        for (size_t t = 0; t < tipos.size(); t++) {
            jsonOutput += "    \"" + tipos[t] + "\": {\n";
            for (size_t s = 0; s < tamanhos.size(); s++) {
                int tamanho = tamanhos[s];
                cout << "\nTipo: " << tipos[t] << " | Tamanho: " << tamanho << " | Gerando " << K_AMOSTRAS << " vetores amostrais...\n";

                vector<vector<int>> vetoresOriginais(K_AMOSTRAS);
                for (int k = 0; k < K_AMOSTRAS; k++) {
                    if (t == 0) vetoresOriginais[k] = generateRandomArray(tamanho, gen);
                    else if (t == 1) vetoresOriginais[k] = generateSortedArray(tamanho);
                    else vetoresOriginais[k] = generateReverseSortedArray(tamanho);
                }

                vector<double> temposExecucoes(K_AMOSTRAS);
                cout << "Executando " << nomes_algoritmos[a] << " (" << K_AMOSTRAS << "x)... ";

                for (int k = 0; k < K_AMOSTRAS; k++) {
                    vector<int> vetorTeste = vetoresOriginais[k];

                    auto start = high_resolution_clock::now();
                    algoritmos[a](vetorTeste);
                    auto stop = high_resolution_clock::now();

                    duration<double> ms = stop - start;
                    temposExecucoes[k] = ms.count();
                }

                double soma = 0.0;
                for (double tempo : temposExecucoes) soma += tempo;
                double media = soma / K_AMOSTRAS;

                double sumOfSquaresOfDifferences = 0.0;
                for (double tempo : temposExecucoes) {
                    sumOfSquaresOfDifferences += (tempo - media) * (tempo - media);
                }
                double desvio = K_AMOSTRAS > 1 ? sqrt(sumOfSquaresOfDifferences / (K_AMOSTRAS - 1)) : 0.0;

                cout << fixed << setprecision(4);
                cout << "[Média: " << media << "s | StdDev: ±" << desvio << "s]\n";

                // Format string to standard decimal point instead of comma if needed
                char buff1[100];
                char buff2[100];
                snprintf(buff1, sizeof(buff1), "%.8f", media);
                snprintf(buff2, sizeof(buff2), "%.8f", desvio);

                jsonOutput += "      \"" + to_string(tamanho) + "\": {\n";
                jsonOutput += "        \"media\": " + string(buff1) + ",\n";
                jsonOutput += "        \"desvio_padrao\": " + string(buff2) + "\n      }";
                
                if (s < tamanhos.size() - 1) jsonOutput += ",";
                jsonOutput += "\n";
            }
            jsonOutput += "    }";
            if (t < tipos.size() - 1) jsonOutput += ",";
            jsonOutput += "\n";
        }
        jsonOutput += "  }";
        if (a < algoritmos.size() - 1) jsonOutput += ",";
        jsonOutput += "\n";
    }
    jsonOutput += "}\n";

    ofstream outFile("resultados_cpp.json");
    if (outFile.is_open()) {
        outFile << jsonOutput;
        outFile.close();
        cout << "\nTestes C++ concluídos. Resultados salvos em 'resultados_cpp.json'.\n";
    } else {
        cout << "\nNão foi possível abrir o arquivo file para escrita!\n";
    }

    return 0;
}
