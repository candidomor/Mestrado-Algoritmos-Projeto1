import random # Módulo nativo para processos estocásticos e geração de números pseudoaleatórios (PRNG).

def generate_random_array(size):
    # Gera um vetor populado com inteiros pseudoaleatórios sob uma distribuição uniforme discreta.
    # Representa instâncias de Caso Médio (average-case) para a avaliação empírica dos algoritmos.
    # A limitação do espaço amostral ao teto de (size * 2) é intencional: ela induz uma probabilidade
    # controlada de colisões (elementos duplicados). Esta característica modela com maior fidelidade
    # a entropia encontrada em conjuntos de dados reais, em contraste com permutações estritamente únicas.
    return [random.randint(0, size * 2) for _ in range(size)]

def generate_sorted_array(size):
    # Gera uma sequência monotonicamente crescente de números inteiros.
    # Modela o Melhor Caso (best-case) teórico para algoritmos de ordenação adaptativos 
    # (como as variantes otimizadas do Bubble Sort e o Insertion Sort), avaliando o custo
    # computacional mínimo quando o número de inversões no arranjo é zero.
    # A materialização do iterador 'range' em memória via 'list()' garante tempo de geração constante O(N).
    return list(range(size))

def generate_reverse_sorted_array(size):
    # Gera uma sequência monotonicamente decrescente de números inteiros.
    # Modela o Pior Caso (worst-case) absoluto para a maioria dos algoritmos baseados em comparação.
    # Nesta configuração, o número de inversões na estrutura de dados é maximizado, forçando
    # os algoritmos (especialmente os de complexidade quadrática) a realizarem o número máximo
    # de permutações e comparações teóricas.
    return list(range(size, 0, -1))