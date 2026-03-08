import json
import matplotlib.pyplot as plt

def plot_charts():
    with open('resultados_mestrado.json', 'r', encoding='utf-8') as f:
        resultados = json.load(f)
        
    tamanhos = [1000, 10000, 100000]
    tipos_vetor = ["Aleatório", "Crescente", "Decrescente"]
    algoritmos = list(resultados.keys())
    
    # Gráficos em Eixo Y Linear (padrão) com ErrorBars
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))
        plt.title(f"Tempo Médio de Execução (Linear) - Vetor {tipo}\nAmostragem k=5 para mitigar ruído SO")
        plt.xlabel("Tamanho do Vetor")
        plt.ylabel("Tempo Médio (segundos)")
        
        for alg in algoritmos:
            medias = [resultados[alg][tipo][str(tamanho)]["media"] for tamanho in tamanhos]
            desvios = [resultados[alg][tipo][str(tamanho)]["desvio_padrao"] for tamanho in tamanhos]
            plt.errorbar(tamanhos, medias, yerr=desvios, marker='o', capsize=5, label=alg)
            
        plt.xscale('log') # Eixo X logarítmico para não aglomerar os 1K e 10K
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(f"grafico_linear_{tipo.lower()}.png")
        plt.close()

    # Gráficos em Eixo Y Logarítmico (destaca as diferenças pequenas entre os mais eficientes)
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))
        plt.title(f"Tempo Médio de Execução (Logarítmico) - Vetor {tipo}")
        plt.xlabel("Tamanho do Vetor")
        plt.ylabel("Tempo Médio (segundos)")
        
        for alg in algoritmos:
            medias = [resultados[alg][tipo][str(tamanho)]["media"] for tamanho in tamanhos]
            medias_seguras = [max(m, 1e-6) for m in medias] 
            # Omitindo yerr em gráficos logarítmicos porque desvios padrão simétricos em Y-Log podem estourar
            plt.plot(tamanhos, medias_seguras, marker='o', label=alg)
            
        plt.xscale('log')
        plt.yscale('log')
        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(f"grafico_log_{tipo.lower()}.png")
        plt.close()

    # Gráficos de Dados "Logarítmicos" com Y em escala Linear (Abismo visual)
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
        plt.savefig(f"grafico_abismo_{tipo.lower()}.png")
        plt.close()

if __name__ == "__main__":
    plot_charts()
    print("Novos gráficos gerados com sucesso baseados na Média e Desvio Padrão (k=5)!")
