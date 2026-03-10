import sys  # Importa o módulo sys para interagir fortemente com o interpretador Python

# Aumentamos o limite de recursão padrão do Python (geralmente 1000) para 2000000.
# Isso é fundamental para evitar que o algoritmo Quick Sort (que é recursivo) gere o erro
# RecursionError: maximum recursion depth exceeded,
# especialmente em piores casos, como quando o vetor já está ordenado ou inversamente ordenado,
# formando uma árvore de recursão muito profunda (estouro da Call Stack).
sys.setrecursionlimit(2000000)

def bubble_sort_padrao(arr):
    # Obtém o tamanho total do vetor (array) para determinar o limite do laço.
    n = len(arr)
    
    # Bubble Sort Padrão (Implementação Didática, sem otimizações)
    # Este laço externo roda 'n' vezes. Ele garante que a passagem flutue os maiores
    # elementos progressivamente para o fim do array.
    for i in range(n):
        # Laço interno: ele ignora os últimos 'i' elementos do array,
        # pois após a iteração 'i', os 'i' maiores elementos já estão na posição correta no final.
        # Ele vai de 0 até (n - i - 1).
        for j in range(0, n - i - 1):
            # Compara o elemento atual 'arr[j]' com o elemento imediatamente à sua direita 'arr[j + 1]'.
            if arr[j] > arr[j + 1]:
                # Se o elemento atual for maior que o próximo (ordem errada), realiza a troca de posições (Swap).
                # Em Python, o truque de atribuição múltipla a, b = b, a permite fazer isso sem varíavel auxiliar.
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def bubble_sort(arr):
    # Obtém o tamanho do vetor para iteração.
    n = len(arr)
    
    # Bubble Sort Melhorado (Early Exit)
    # Inclui uma flag (sinalizador) para saber se a lista já está ordenada e parar antecipadamente.
    for i in range(n):
        # A flag 'swapped' inicia como False a cada nova passagem. Ela assumirá True se ocorrer ao menos uma troca.
        swapped = False
        
        # O laço interno percorre do começo até os elementos que ainda não foram ordenados.
        for j in range(0, n - i - 1):
            # Compara o elemento atual com o próximo.
            if arr[j] > arr[j + 1]:
                # Como estão fora de ordem, ocorre o Swap (troca).
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                # Sinaliza que uma troca ocorreu nesta passagem inteira pelo laço.
                swapped = True
                
        # Após passar por todos os itens adjacentes, se nenhuma troca (swap) ocorreu (a flag ainda é False),
        # significa que os elementos já estão todos em ordem (Cenário Melhor Caso: O(n)).
        if not swapped:
            # Comando de quebra do laço 'for i', interrompendo iterações desnecessárias economizando tempo.
            break

def selection_sort(arr):
    # Obtém o tamanho da lista. O Selection Sort sempre dividirá conceitualmente o vetor 
    # em duas partes: subarray ordenado à esquerda e subarray desordenado à direita.
    n = len(arr)
    
    # O laço avança a borda do subarray ordenado passo a passo para a direita.
    for i in range(n):
        # Assume provisoriamente que o primeiro elemento da porção desordenada (índice 'i') é o menor (Mínimo).
        min_idx = i
        
        # O laço interno varre unicamente o restante do vetor não ordenado (de i+1 até n).
        for j in range(i + 1, n):
            # Se encontrar um elemento menor do que o mínimo assumido atualmente...
            if arr[min_idx] > arr[j]:
                # Atualiza a referência de índice do menor elemento encontrado até agora.
                min_idx = j
                
        # Terminada a varredura e encontrado o índice absoluto do menor elemento,
        # troca o primeiro elemento da porção desordenada 'arr[i]' com este menor elemento 'arr[min_idx]'.
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    # O Insertion Sort imagina que o 1º item (índice 0) constitui uma lista já ordenada.
    # Por isso, o for começa a partir do 2º item (índice 1) até o final.
    for i in range(1, len(arr)):
        # Guarda o valor do elemento a ser posicionado (A Chave atual).
        key = arr[i]
        
        # 'j' representa o último índice da "porção já ordenada"
        j = i - 1
        
        # Este 'while' busca a posição correta da chave varrendo a porção ordenada de trás para frente.
        # Condição 1: Não cheguei no início do array (j >= 0).
        # Condição 2: O item atual varrido (arr[j]) é maior do que a minha chave?
        while j >= 0 and key < arr[j]:
            # Como arr[j] é maior, eu arrasto ele uma casa para a direita abriando espaço para a chave.
            arr[j + 1] = arr[j]
            # Decrementa o j para continuar olhando os vizinhos à esquerda.
            j -= 1
            
        # Quando o while termina (seja por chegar a j=-1 ou achar algum vizinho menor que a chave),
        # a posição (j + 1) será exatamente o buraco (espaço vazio) onde a chave pertence.
        arr[j + 1] = key

def merge_sort(arr):
    # Algoritmo Base de Divisão e Conquista.
    # O Caso Base recursivo acontece se a lista for vazia ou ter 1 tamanho (sendo inerentemente ordenada).
    if len(arr) > 1:
        # Encontra o índice central (Meio) cortando as casas decimais com '//'
        mid = len(arr) // 2
        
        # (Divisão) Fatia (slicing) a lista em duas sublistas:
        # L (Left): Pega os elementos do começo (0) até o meio-1.
        L = arr[:mid]
        # R (Right): Pega elementos a partir do meio até o fim (n-1).
        R = arr[mid:]

        # Chama a si mesmo (Recursão) para dividir a metade esquerda até que todo 'L' tenha 1 item.
        merge_sort(L)
        # Chama a si mesmo para dividir a metade direita até que ela também tenha 1 item.
        merge_sort(R)

        # Início do Passo de Conquista (Merge/Intercalação).
        i = j = k = 0 # i: iterador de L  |  j: iterador de R |  k: iterador do vetor mesclado global.

        # Enquanto nenhuma das metades for inteiramente percorrida:
        while i < len(L) and j < len(R):
            # Compara o menor elemento atual de L contra o menor de R
            if L[i] < R[j]:
                # L contém o menor item: coloca ele na posição K do array original
                arr[k] = L[i]
                # Avança a janela pra ler o próximo valor de L
                i += 1
            else:
                # R contém o menor (ou igual).
                arr[k] = R[j]
                # Avança a janela pra ler o próximo valor de R
                j += 1
            # Independentemente de quem preencheu, o ponteiro de construção avança a casa.
            k += 1

        # Uma vez que o laco anterior acabar, alguma das metades vai esgotar primeiro.
        # Assim, devemos "despejar" os sobreviventes da metade que restou.

        # Recolhe sobras residuais eventuais do vetor Esquerdo L.
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        # Recolhe sobras residuais eventuais do vetor Direito R.
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def quick_sort(arr):
    # Wrapper function (Função Envoltória / Ponto de Entrada) para o Quick Sort.
    # Facilita a chamada inicial ocultando os ponteiros internos, delegando a ordenação a _quick_sort
    # passando os ponteiros extremos do array: low = 0 e high = tamanho - 1.
    _quick_sort(arr, 0, len(arr) - 1)

def _quick_sort(arr, low, high):
    # O motor recursivo interno do Quick Sort. Funciona no modelo Divide-and-Conquer.
    # Caso base: para a recursão quando as fronteiras e cruzam (lista vazia ou unitária).
    if low < high:
        # O particionamento reorganiza a lista na fronteira atual (low..high) escolhendo um pivô,
        # e joga os menores à esquerda e maiores à direita dele.
        # Ele retorna 'pi' (partition index), o lugar exato, e final, do pivô atual no array.
        pi = partition(arr, low, high)
        
        # Dispara uma divisão recursiva para a ala dos elementos menores que o pivô.
        _quick_sort(arr, low, pi - 1)
        # Dispara uma divisão recursiva para a ala dos elementos maiores que o pivô.
        _quick_sort(arr, pi + 1, high)

def partition(arr, low, high):
    # A mecânica que confere a magia do pivô ao algoritmo Quick Sort.
    
    # Prevenção O(n^2): em Python clássico usar o último como pivô falha catastroficamente (e estoira memória)
    # caso as listas sejam previamente ordenadas. Para contornar e aproximar do custo de n*log(n):
    # Selecionamos o elemento do meio como Pivô lógico.
    mid = low + (high - low) // 2
    
    # Feita a seleção, trocamos (Swap) esse elemento do Meio pelo o do canto final (high).
    # Assim aplicamos os métodos convencionais de varredura usando o ponteiro de canto.
    arr[mid], arr[high] = arr[high], arr[mid]
    
    # Declaramos o pivô que vai reger as comparações (agora fisicamente ancorado no extremo direito).
    pivot = arr[high]
    
    # Apontador iterativo (i) aponta sempre para o final da "zona dos menores que o pivô".
    # Ele começa uma casa antes do ponto inicial porque a zona dos menores ainda é vazia.
    i = low - 1
    
    # Laço for que varrre os itens entre low até high-1. O high não é incluso pois ele É o pivô.
    for j in range(low, high):
        # Se um elemento atual é estritamente menor que o nosso Pivô regente:
        if arr[j] < pivot:
            # Temos que aumentar o perímetro da "zona dos menores"
            i = i + 1
            # E trazer esse elemento que encontramos lá pra dentro desta zona (swap entre arr[i] e arr[j]).
            arr[i], arr[j] = arr[j], arr[i]
            
    # Ao final da varredura, sabemos que o limite que divide "menores" e "maiores" repousa em 'i'.
    # Dessa forma, trocamos o pivô 'arr[high]' descolando-o do canto direito direto pro centro exato (i+1). 
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    # Retornamos o índice definitivo (i+1) onde o Pivô encostou; esse cara nunca mais será movido.
    return i + 1
