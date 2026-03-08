import java.util.*;
import java.io.*;
import java.nio.file.*;

public class Benchmark {

    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            boolean swapped = false;
            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            if (!swapped) break;
        }
    }

    public static void selectionSort(int[] arr) {
        int n = arr.length;
        for (int i = 0; i < n; i++) {
            int min_idx = i;
            for (int j = i + 1; j < n; j++) {
                if (arr[min_idx] > arr[j]) {
                    min_idx = j;
                }
            }
            int temp = arr[i];
            arr[i] = arr[min_idx];
            arr[min_idx] = temp;
        }
    }

    public static void insertionSort(int[] arr) {
        int n = arr.length;
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

    public static void merge(int[] arr, int[] temp, int left, int mid, int right) {
        for (int x = left; x <= right; x++) {
            temp[x] = arr[x];
        }
        int i = left;
        int j = mid + 1;
        int k = left;
        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                arr[k] = temp[i];
                i++;
            } else {
                arr[k] = temp[j];
                j++;
            }
            k++;
        }
        while (i <= mid) {
            arr[k] = temp[i];
            k++;
            i++;
        }
    }

    public static void mergeSortRecursive(int[] arr, int[] temp, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSortRecursive(arr, temp, left, mid);
            mergeSortRecursive(arr, temp, mid + 1, right);
            merge(arr, temp, left, mid, right);
        }
    }

    public static void mergeSort(int[] arr) {
        int[] temp = new int[arr.length];
        mergeSortRecursive(arr, temp, 0, arr.length - 1);
    }

    public static int partition(int[] arr, int low, int high) {
        int mid = low + (high - low) / 2;
        int t1 = arr[mid]; arr[mid] = arr[high]; arr[high] = t1;
        
        int pivot = arr[high];
        int i = (low - 1);
        for (int j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
        int t2 = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = t2;
        return i + 1;
    }

    public static void quickSortRecursive(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSortRecursive(arr, low, pi - 1);
            quickSortRecursive(arr, pi + 1, high);
        }
    }

    public static void quickSort(int[] arr) {
        quickSortRecursive(arr, 0, arr.length - 1);
    }

    public static int[] generateRandomArray(int size, Random rnd) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) {
            arr[i] = rnd.nextInt(size * 2);
        }
        return arr;
    }

    public static int[] generateSortedArray(int size) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) arr[i] = i;
        return arr;
    }

    public static int[] generateReverseSortedArray(int size) {
        int[] arr = new int[size];
        for (int i = 0; i < size; i++) arr[i] = size - i;
        return arr;
    }

    public interface SortFunction {
        void sort(int[] arr);
    }

    public static void main(String[] args) {
        int[] tamanhos = { 1000, 10000, 100000 };
        int K_AMOSTRAS = 5;
        String[] tipos = { "Aleatório", "Crescente", "Decrescente" };
        String[] nomes_algoritmos = { "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort" };

        SortFunction[] algoritmos = {
            Benchmark::bubbleSort,
            Benchmark::selectionSort,
            Benchmark::insertionSort,
            Benchmark::mergeSort,
            Benchmark::quickSort
        };

        Random rnd = new Random(42);

        System.out.println("Iniciando bateria de testes Java (JVM) (" + K_AMOSTRAS + " amostras).");

        StringBuilder jsonOutput = new StringBuilder("{\n");

        for (int a = 0; a < algoritmos.length; a++) {
            jsonOutput.append("  \"").append(nomes_algoritmos[a]).append("\": {\n");
            for (int t = 0; t < tipos.length; t++) {
                jsonOutput.append("    \"").append(tipos[t]).append("\": {\n");
                for (int s = 0; s < tamanhos.length; s++) {
                    int tamanho = tamanhos[s];
                    System.out.printf("\nTipo: %s | Tamanho: %d | Gerando %d vetores amostrais...\n", tipos[t], tamanho, K_AMOSTRAS);

                    List<int[]> vetoresOriginais = new ArrayList<>();
                    for (int k = 0; k < K_AMOSTRAS; k++) {
                        if (t == 0) vetoresOriginais.add(generateRandomArray(tamanho, rnd));
                        else if (t == 1) vetoresOriginais.add(generateSortedArray(tamanho));
                        else vetoresOriginais.add(generateReverseSortedArray(tamanho));
                    }

                    double[] temposExecucoes = new double[K_AMOSTRAS];
                    System.out.printf("Executando %s (%dx)... ", nomes_algoritmos[a], K_AMOSTRAS);

                    for (int k = 0; k < K_AMOSTRAS; k++) {
                        int[] vetorTeste = Arrays.copyOf(vetoresOriginais.get(k), tamanho);

                        long start = System.nanoTime();
                        algoritmos[a].sort(vetorTeste);
                        long stop = System.nanoTime();

                        temposExecucoes[k] = (stop - start) / 1_000_000_000.0;
                    }

                    double media = Arrays.stream(temposExecucoes).average().orElse(0.0);
                    double sumOfSquares = 0.0;
                    for (double tempo : temposExecucoes) {
                        sumOfSquares += (tempo - media) * (tempo - media);
                    }
                    double desvio = K_AMOSTRAS > 1 ? Math.sqrt(sumOfSquares / (K_AMOSTRAS - 1)) : 0.0;

                    System.out.printf(Locale.US, "[Média: %.4fs | StdDev: ±%.4fs]\n", media, desvio);

                    jsonOutput.append("      \"").append(tamanho).append("\": {\n")
                              .append("        \"media\": ").append(String.format(Locale.US, "%.8f", media)).append(",\n")
                              .append("        \"desvio_padrao\": ").append(String.format(Locale.US, "%.8f", desvio)).append("\n      }");

                    if (s < tamanhos.length - 1) jsonOutput.append(",");
                    jsonOutput.append("\n");
                }
                jsonOutput.append("    }");
                if (t < tipos.length - 1) jsonOutput.append(",");
                jsonOutput.append("\n");
            }
            jsonOutput.append("  }");
            if (a < algoritmos.length - 1) jsonOutput.append(",");
            jsonOutput.append("\n");
        }
        jsonOutput.append("}\n");

        try {
            Files.write(Paths.get("resultados_java.json"), jsonOutput.toString().getBytes());
            System.out.println("\nTestes Java concluídos. Resultados salvos em 'resultados_java.json'.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
