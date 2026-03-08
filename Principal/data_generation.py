import random

def generate_random_array(size):
    # Geração de inteiros aleatórios na faixa de 0 a size*2 para haver alguma repetição
    return [random.randint(0, size * 2) for _ in range(size)]

def generate_sorted_array(size):
    return list(range(size))

def generate_reverse_sorted_array(size):
    return list(range(size, 0, -1))
