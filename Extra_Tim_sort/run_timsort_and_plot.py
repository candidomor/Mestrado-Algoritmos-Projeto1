import sys
import os
import time
import json
import statistics
import matplotlib.pyplot as plt

# Adicionar o diretório Principal ao path para importar data_generation
dir_atual = os.path.dirname(os.path.abspath(__file__))
dir_principal = os.path.join(os.path.dirname(dir_atual), "Principal")
sys.path.append(dir_principal)

from data_generation import generate_random_array, generate_sorted_array, generate_reverse_sorted_array

def timsort_wrapper(arr):
    arr.sort()

def main():
    tamanhos = [1000, 10000, 100000]
    K_AMOSTRAS = 5

    tipos_vetor = {
        "Aleatório": generate_random_array,
        "Crescente": generate_sorted_array,
        "Decrescente": generate_reverse_sorted_array
    }

    # Carregar resultados anteriores
    arquivo_resultados_anteriores = os.path.join(dir_principal, "resultados_mestrado.json")
    with open(arquivo_resultados_anteriores, 'r', encoding='utf-8') as f:
        resultados = json.load(f)

    # Inicializar os resultados do Timsort
    nome_alg = "Timsort (Nativo)"
    resultados[nome_alg] = {tipo: {str(tamanho): {"media": 0, "desvio_padrao": 0} for tamanho in tamanhos} for tipo in tipos_vetor}

    print(f"Iniciando testes com Timsort Nativo (k={K_AMOSTRAS})...")

    for tamanho in tamanhos:
        print(f"\n{'='*40}\n--- Tamanho do vetor: {tamanho} ---\n{'='*40}")
        for tipo, func_geradora in tipos_vetor.items():
            print(f"\nTipo: {tipo} | Gerando {K_AMOSTRAS} vetores amostrais...")
            
            # Gerando arrays base
            vetores_originais = [func_geradora(tamanho) for _ in range(K_AMOSTRAS)]
            tempos_execucoes = []
            
            print(f"Executando {nome_alg}...", end=" ", flush=True)

            for iteracao in range(K_AMOSTRAS):
                vetor_teste = list(vetores_originais[iteracao])
                
                inicio = time.perf_counter()
                timsort_wrapper(vetor_teste)
                fim = time.perf_counter()
                
                tempos_execucoes.append(fim - inicio)
            
            media = statistics.mean(tempos_execucoes)
            desvio = statistics.stdev(tempos_execucoes) if K_AMOSTRAS > 1 else 0.0

            resultados[nome_alg][tipo][str(tamanho)]["media"] = media
            resultados[nome_alg][tipo][str(tamanho)]["desvio_padrao"] = desvio
            
            print(f"[Média: {media:.6f}s | StdDev: ±{desvio:.6f}s]")

    # Salvar novo JSON
    arquivo_novo_json = os.path.join(dir_atual, "resultados_com_timsort.json")
    with open(arquivo_novo_json, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)
    
    print(f"\nResultados combinados salvos em '{arquivo_novo_json}'.")

    print("\nGerando Gráficos Comparativos...")
    algoritmos = list(resultados.keys())
    
    # 1. Gráficos em Eixo Y Linear com ErrorBars
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))
        plt.title(f"Tempo Médio de Execução (Linear) - Vetor {tipo}\nAmostragem k={K_AMOSTRAS} para mitigar ruído SO")
        plt.xlabel("Tamanho do Vetor")
        plt.ylabel("Tempo Médio (segundos)")
        
        for alg in algoritmos:
            medias = [resultados[alg][tipo][str(tamanho)]["media"] for tamanho in tamanhos]
            desvios = [resultados[alg][tipo][str(tamanho)]["desvio_padrao"] for tamanho in tamanhos]
            plt.errorbar(tamanhos, medias, yerr=desvios, marker='o', capsize=5, label=alg)
            
        plt.xscale('log') # Eixo X logarítmico
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(os.path.join(dir_atual, f"grafico_linear_{tipo.lower()}.png"))
        plt.close()

    # 2. Gráficos em Eixo Y Logarítmico
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))
        plt.title(f"Tempo Médio de Execução (Logarítmico) - Vetor {tipo}")
        plt.xlabel("Tamanho do Vetor")
        plt.ylabel("Tempo Médio (segundos)")
        
        for alg in algoritmos:
            medias = [resultados[alg][tipo][str(tamanho)]["media"] for tamanho in tamanhos]
            medias_seguras = [max(m, 1e-6) for m in medias] 
            plt.plot(tamanhos, medias_seguras, marker='o', label=alg)
            
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(os.path.join(dir_atual, f"grafico_log_{tipo.lower()}.png"))
        plt.close()

    # 3. Gráficos de Dados "Logarítmicos" com Y em escala Linear (Abismo visual)
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))
        plt.title(f"Tempo Médio de Execução (Abismo Vertical) - Vetor {tipo}")
        plt.xlabel("Tamanho do Vetor (Escala Log X)")
        plt.ylabel("Tempo Médio (segundos, Escala Linear Y)")
        
        for alg in algoritmos:
            medias = [resultados[alg][tipo][str(tamanho)]["media"] for tamanho in tamanhos]
            desvios = [resultados[alg][tipo][str(tamanho)]["desvio_padrao"] for tamanho in tamanhos]
            plt.errorbar(tamanhos, medias, yerr=desvios, marker='o', capsize=5, label=alg)
            
        plt.xscale('log')
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(os.path.join(dir_atual, f"grafico_abismo_{tipo.lower()}.png"))
        plt.close()

    print("Novos gráficos gerados com sucesso na pasta 'Extra_Tim_sort'!")

if __name__ == "__main__":
    main()
