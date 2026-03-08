import time
import json
import sys
import statistics
import os
import shutil
from datetime import datetime
from sorting_algorithms import *
from data_generation import *

def backup_resultados_anteriores():
    dir_principal = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_principal)
    dir_backup = os.path.join(dir_raiz, "Backup_Python")
    
    if not os.path.exists(dir_backup):
        os.makedirs(dir_backup)
        
    arquivos_alvo = ["resultados_mestrado.json", "Relatorio_Projeto1.md"]
    if os.path.exists(dir_principal):
        for nome in os.listdir(dir_principal):
            if nome.startswith("grafico_") and nome.endswith(".png"):
                arquivos_alvo.append(nome)
                
    arquivos_existentes = [f for f in list(set(arquivos_alvo)) if os.path.exists(os.path.join(dir_principal, f))]
    
    if arquivos_existentes:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pasta_dest = os.path.join(dir_backup, f"Execucao_{timestamp}")
        os.makedirs(pasta_dest)
        
        for arquivo in arquivos_existentes:
            caminho_origem = os.path.join(dir_principal, arquivo)
            caminho_dest = os.path.join(pasta_dest, arquivo)
            # Usamos copy2 (copiar) em vez de move (mover) para preservar o Relatorio.md original para que você não precise recriá-lo
            shutil.copy2(caminho_origem, caminho_dest)
        
        print(f"[*] Backup da execução anterior salvo em: Backup_Python\\Execucao_{timestamp}\n")

def main():
    backup_resultados_anteriores()
    algoritmos = {
        "Bubble Sort Padrão": bubble_sort_padrao,
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    tamanhos = [1000, 10000, 100000]
    K_AMOSTRAS = 5 # Quantidade de repetições para rigor estatístico

    tipos_vetor = {
        "Aleatório": generate_random_array,
        "Crescente": generate_sorted_array,
        "Decrescente": generate_reverse_sorted_array
    }

    # Estrutura JSON com dicionário aninhado guardando as métricas estatísticas
    resultados = {nome_alg: {tipo: {str(tamanho): {"media": 0, "desvio_padrao": 0} for tamanho in tamanhos} for tipo in tipos_vetor} for nome_alg in algoritmos}

    print(f"Iniciando bateria de testes com Rigor Estatístico (k={K_AMOSTRAS} amostras).")

    for tamanho in tamanhos:
        print(f"\n{'='*40}\n--- Tamanho do vetor: {tamanho} ---\n{'='*40}")
        for tipo, func_geradora in tipos_vetor.items():
            print(f"\nTipo: {tipo} | Gerando {K_AMOSTRAS} vetores amostrais...")
            
            # Gerado k vetores base diferentes para evitar cache e aleatoriedade "viciada" na amostragem
            vetores_originais = [func_geradora(tamanho) for _ in range(K_AMOSTRAS)]
            
            for nome_alg, func_ord in algoritmos.items():
                tempos_execucoes = []
                print(f"Executando {nome_alg} ({K_AMOSTRAS}x)...", end=" ", flush=True)

                for iteracao in range(K_AMOSTRAS):
                    vetor_teste = list(vetores_originais[iteracao]) # Shallow copy limpa do array k
                    
                    inicio = time.perf_counter()
                    func_ord(vetor_teste)
                    fim = time.perf_counter()
                    
                    tempos_execucoes.append(fim - inicio)
                
                media = statistics.mean(tempos_execucoes)
                # Para k=1, desvio padrão não existe, trataremos isso com um float de segurança
                desvio = statistics.stdev(tempos_execucoes) if K_AMOSTRAS > 1 else 0.0

                resultados[nome_alg][tipo][str(tamanho)]["media"] = media
                resultados[nome_alg][tipo][str(tamanho)]["desvio_padrao"] = desvio
                
                print(f"[Média: {media:.4f}s | StdDev: ±{desvio:.4f}s]")

    # Salvando os resultados
    with open('resultados_mestrado.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("\nTodos os testes estatísticos concluídos. Resultados salvos em 'resultados_mestrado.json'.")

if __name__ == "__main__":
    main()
