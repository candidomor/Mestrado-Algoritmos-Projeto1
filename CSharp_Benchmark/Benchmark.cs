using System;
using System.Diagnostics;
using System.IO;
using System.Globalization;
using System.Collections.Generic;
using System.Linq;

namespace SortingBenchmark
{
    class Program
    {
        static void BubbleSort(int[] arr)
        {
            int n = arr.Length;
            for (int i = 0; i < n; i++)
            {
                bool swapped = false;
                for (int j = 0; j < n - i - 1; j++)
                {
                    if (arr[j] > arr[j + 1])
                    {
                        int temp = arr[j];
                        arr[j] = arr[j + 1];
                        arr[j + 1] = temp;
                        swapped = true;
                    }
                }
                if (!swapped) break;
            }
        }

        static void SelectionSort(int[] arr)
        {
            int n = arr.Length;
            for (int i = 0; i < n; i++)
            {
                int min_idx = i;
                for (int j = i + 1; j < n; j++)
                {
                    if (arr[min_idx] > arr[j])
                    {
                        min_idx = j;
                    }
                }
                int temp = arr[i];
                arr[i] = arr[min_idx];
                arr[min_idx] = temp;
            }
        }

        static void InsertionSort(int[] arr)
        {
            int n = arr.Length;
            for (int i = 1; i < n; i++)
            {
                int key = arr[i];
                int j = i - 1;
                while (j >= 0 && arr[j] > key)
                {
                    arr[j + 1] = arr[j];
                    j = j - 1;
                }
                arr[j + 1] = key;
            }
        }

        static void MergeSort(int[] arr)
        {
            int[] temp = new int[arr.Length];
            MergeSortRecursive(arr, temp, 0, arr.Length - 1);
        }

        static void MergeSortRecursive(int[] arr, int[] temp, int left, int right)
        {
            if (left < right)
            {
                int mid = left + (right - left) / 2;
                MergeSortRecursive(arr, temp, left, mid);
                MergeSortRecursive(arr, temp, mid + 1, right);
                Merge(arr, temp, left, mid, right);
            }
        }

        static void Merge(int[] arr, int[] temp, int left, int mid, int right)
        {
            for (int x = left; x <= right; x++)
                temp[x] = arr[x];

            int i = left;
            int j = mid + 1;
            int k = left;

            while (i <= mid && j <= right)
            {
                if (temp[i] <= temp[j])
                {
                    arr[k] = temp[i];
                    i++;
                }
                else
                {
                    arr[k] = temp[j];
                    j++;
                }
                k++;
            }

            while (i <= mid)
            {
                arr[k] = temp[i];
                k++;
                i++;
            }
        }

        static void QuickSort(int[] arr)
        {
            QuickSortRecursive(arr, 0, arr.Length - 1);
        }

        static void QuickSortRecursive(int[] arr, int low, int high)
        {
            if (low < high)
            {
                int pi = Partition(arr, low, high);
                QuickSortRecursive(arr, low, pi - 1);
                QuickSortRecursive(arr, pi + 1, high);
            }
        }

        static int Partition(int[] arr, int low, int high)
        {
            int mid = low + (high - low) / 2;
            int t1 = arr[mid]; arr[mid] = arr[high]; arr[high] = t1;

            int pivot = arr[high];
            int i = (low - 1);
            for (int j = low; j < high; j++)
            {
                if (arr[j] < pivot)
                {
                    i++;
                    int temp = arr[i];
                    arr[i] = arr[j];
                    arr[j] = temp;
                }
            }
            int t2 = arr[i + 1]; arr[i + 1] = arr[high]; arr[high] = t2;
            return i + 1;
        }

        static int[] GenerateRandomArray(int size, Random rnd)
        {
            int[] arr = new int[size];
            for (int i = 0; i < size; i++) arr[i] = rnd.Next(0, size * 2);
            return arr;
        }

        static int[] GenerateSortedArray(int size)
        {
            int[] arr = new int[size];
            for (int i = 0; i < size; i++) arr[i] = i;
            return arr;
        }

        static int[] GenerateReverseSortedArray(int size)
        {
            int[] arr = new int[size];
            for (int i = 0; i < size; i++) arr[i] = size - i;
            return arr;
        }

        static void Main(string[] args)
        {
            int[] tamanhos = { 1000, 10000, 100000 };
            int K_AMOSTRAS = 5;
            string[] tipos = { "Aleatório", "Crescente", "Decrescente" };
            string[] algoritmos = { "Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort" };
            
            Action<int[]>[] funcs = { BubbleSort, SelectionSort, InsertionSort, MergeSort, QuickSort };
            
            Random rnd = new Random(42);
            
            Console.WriteLine("Iniciando bateria de testes C# nativo (" + K_AMOSTRAS + " amostras).");

            string jsonOutput = "{\n";

            for (int a = 0; a < algoritmos.Length; a++)
            {
                jsonOutput += "  \"" + algoritmos[a] + "\": {\n";
                for (int t = 0; t < tipos.Length; t++)
                {
                    jsonOutput += "    \"" + tipos[t] + "\": {\n";
                    for (int s = 0; s < tamanhos.Length; s++)
                    {
                        int tamanho = tamanhos[s];
                        Console.WriteLine("\nTipo: " + tipos[t] + " | Tamanho: " + tamanho + " | Gerando " + K_AMOSTRAS + " vetores amostrais...");
                        
                        List<int[]> vetoresOriginais = new List<int[]>();
                        for (int k = 0; k < K_AMOSTRAS; k++)
                        {
                            if (t == 0) vetoresOriginais.Add(GenerateRandomArray(tamanho, rnd));
                            else if (t == 1) vetoresOriginais.Add(GenerateSortedArray(tamanho));
                            else vetoresOriginais.Add(GenerateReverseSortedArray(tamanho));
                        }

                        List<double> temposExecucoes = new List<double>();
                        Console.Write("Executando " + algoritmos[a] + " (" + K_AMOSTRAS + "x)... ");

                        for (int k = 0; k < K_AMOSTRAS; k++)
                        {
                            int[] vetorTeste = new int[tamanho];
                            Array.Copy(vetoresOriginais[k], vetorTeste, tamanho);

                            Stopwatch sw = Stopwatch.StartNew();
                            funcs[a](vetorTeste);
                            sw.Stop();

                            temposExecucoes.Add(sw.Elapsed.TotalSeconds);
                        }

                        double media = temposExecucoes.Average();
                        double sumOfSquaresOfDifferences = temposExecucoes.Select(val => (val - media) * (val - media)).Sum();
                        double desvio = K_AMOSTRAS > 1 ? Math.Sqrt(sumOfSquaresOfDifferences / (K_AMOSTRAS - 1)) : 0.0;

                        Console.WriteLine("[Média: " + media.ToString("F4", CultureInfo.InvariantCulture) + "s | StdDev: ±" + desvio.ToString("F4", CultureInfo.InvariantCulture) + "s]");

                        jsonOutput += "      \"" + tamanho + "\": {\n        \"media\": " + media.ToString(CultureInfo.InvariantCulture) + ",\n        \"desvio_padrao\": " + desvio.ToString(CultureInfo.InvariantCulture) + "\n      }";
                        if (s < tamanhos.Length - 1) jsonOutput += ",";
                        jsonOutput += "\n";
                    }
                    jsonOutput += "    }";
                    if (t < tipos.Length - 1) jsonOutput += ",";
                    jsonOutput += "\n";
                }
                jsonOutput += "  }";
                if (a < algoritmos.Length - 1) jsonOutput += ",";
                jsonOutput += "\n";
            }
            jsonOutput += "}\n";

            File.WriteAllText("resultados_csharp.json", jsonOutput);
            Console.WriteLine("\nTestes C# concluídos. Resultados salvos em 'resultados_csharp.json'.");
        }
    }
}
