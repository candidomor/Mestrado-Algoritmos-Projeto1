import sys

# Aumentar o limite de recursão para o QuickSort em piores casos (vetores ordenados/inversos)
sys.setrecursionlimit(2000000)

def bubble_sort_padrao(arr):
    n = len(arr)
    # Bubble Sort Padrão (Sem Melhoria)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def bubble_sort(arr):
    n = len(arr)
    # Bubble Sort Melhorado
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx] > arr[j]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    _quick_sort(arr, 0, len(arr) - 1)

def _quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        _quick_sort(arr, low, pi - 1)
        _quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    # Escolhendo o elemento do meio como pivô para evitar erro de recursão (estouro de pilha) e lentidão O(n^2) em vetores já ordenados
    mid = low + (high - low) // 2
    arr[mid], arr[high] = arr[high], arr[mid]
    
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
