"""
Análise Empírica de Algoritmos – Geração de Gráficos de Desempenho

Contexto: Disciplina de Algoritmos e Programação (Mestrado em Ciência da Computação)

Objetivo:
Gerar visualizações do tempo de execução de diferentes algoritmos de ordenação a partir
de resultados experimentais previamente coletados. A análise empírica permite observar
como o custo computacional evolui conforme o tamanho da entrada, possibilitando
comparações com as classes de complexidade assintótica previstas teoricamente
(Big-O) para diferentes instâncias de dados.
"""

# Biblioteca padrão do Python utilizada para leitura e manipulação de dados
# estruturados no formato JSON, empregados para armazenar os resultados experimentais.
import json

# Biblioteca amplamente utilizada para visualização científica em Python.
# O módulo pyplot fornece uma interface de excelente qualidade para geração de gráficos
# e representações visuais dos dados experimentais.
import matplotlib.pyplot as plt


def plot_charts():
    # Carregamento dos resultados experimentais previamente coletados.
    # Os dados são armazenados em formato JSON para facilitar a persistência
    # estruturada dos resultados obtidos durante as execuções dos algoritmos.
    with open('resultados_mestrado.json', 'r', encoding='utf-8') as f:
        resultados = json.load(f)

    # Tamanhos das instâncias de entrada avaliadas.
    # A escolha de valores em progressão geométrica (potências de 10) permite
    # observar de forma mais clara a tendência de crescimento do tempo de execução.
    tamanhos = [1000, 10000, 100000]

    # Tipos de vetores utilizados nos experimentos.
    # Diferentes distribuições de entrada permitem avaliar o comportamento dos
    # algoritmos em cenários que podem representar melhor caso, pior caso ou
    # comportamento médio, dependendo das características de cada algoritmo.
    tipos_vetor = ["Aleatório", "Crescente", "Decrescente"]

    # Lista de algoritmos avaliados (extraída das chaves do JSON).
    algoritmos = list(resultados.keys())

    # -------------------------------------------------------------------------
    # 1. Gráficos em Escala Linear (Avaliação direta do tempo de execução)
    # -------------------------------------------------------------------------
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))

        # O uso de múltiplas execuções (k repetições) é uma prática comum em
        # experimentos computacionais, pois reduz o impacto de variabilidade
        # introduzida por fatores externos como escalonamento do sistema
        # operacional, efeitos de cache e outras interferências do ambiente.
        plt.title(
            f"Tempo Médio de Execução (Escala Linear) - Vetor {tipo}\n"
            "Amostragem com k=5 execuções para redução de ruído experimental"
        )
        plt.xlabel("Tamanho do Vetor (N)")
        plt.ylabel("Tempo médio de execução (segundos)")

        for alg in algoritmos:
            # Extração das métricas estatísticas registradas para cada tamanho de entrada.
            # A média representa a tendência central do tempo de execução,
            # enquanto o desvio padrão fornece uma estimativa da variabilidade
            # observada nas execuções repetidas.
            medias = [
                resultados[alg][tipo][str(tamanho)]["media"]
                for tamanho in tamanhos
            ]

            desvios = [
                resultados[alg][tipo][str(tamanho)]["desvio_padrao"]
                for tamanho in tamanhos
            ]

            # As barras de erro representam a dispersão observada nos experimentos,
            # permitindo visualizar a estabilidade das medições obtidas.
            plt.errorbar(
                tamanhos,
                medias,
                yerr=desvios,
                marker='o',
                capsize=5,
                label=alg
            )

        # A escala logarítmica no eixo X preserva o espaçamento visual entre
        # instâncias de entrada que crescem em progressão geométrica.
        plt.xscale('log')

        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(f"grafico_linear_{tipo.lower()}.png")
        plt.close()

    # -------------------------------------------------------------------------
    # 2. Gráficos em Escala Log-Log (Análise de classes de complexidade)
    # -------------------------------------------------------------------------
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))

        # Gráficos em escala logarítmica nos dois eixos são frequentemente
        # utilizados na literatura para comparar algoritmos com diferentes
        # classes de complexidade. Em particular, funções polinomiais do tipo
        # O(N^c) tendem a aparecer como retas cuja inclinação está relacionada
        # ao expoente c.
        plt.title(f"Tempo Médio de Execução (Escala Log-Log) - Vetor {tipo}")
        plt.xlabel("Tamanho do Vetor (N)")
        plt.ylabel("Tempo médio de execução (segundos)")

        for alg in algoritmos:
            medias = [
                resultados[alg][tipo][str(tamanho)]["media"]
                for tamanho in tamanhos
            ]

            # Ajuste de limite inferior para evitar valores nulos ou
            # extremamente próximos de zero, uma vez que log(0) é indefinido.
            medias_seguras = [max(m, 1e-6) for m in medias]

            # Neste gráfico opta-se por não incluir barras de erro, pois a
            # interpretação do desvio padrão em escalas logarítmicas pode
            # gerar distorções visuais ou limites inconsistentes.
            plt.plot(
                tamanhos,
                medias_seguras,
                marker='o',
                label=alg
            )

        plt.xscale('log')
        plt.yscale('log')

        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(f"grafico_log_{tipo.lower()}.png")
        plt.close()

    # -------------------------------------------------------------------------
    # 3. Gráficos comparativos destacando discrepâncias de desempenho
    # -------------------------------------------------------------------------
    for tipo in tipos_vetor:
        plt.figure(figsize=(10, 6))

        # Este gráfico enfatiza visualmente a diferença de desempenho entre
        # algoritmos com classes de complexidade distintas. Em particular,
        # algoritmos quadráticos tendem a apresentar crescimento abrupto
        # do tempo de execução quando comparados a algoritmos com
        # complexidade O(N log N).
        plt.title(f"Tempo Médio de Execução (Comparação de Escala) - Vetor {tipo}")
        plt.xlabel("Tamanho do Vetor N (Escala Logarítmica)")
        plt.ylabel("Tempo médio de execução (segundos)")

        for alg in algoritmos:
            medias = [
                resultados[alg][tipo][str(tamanho)]["media"]
                for tamanho in tamanhos
            ]

            desvios = [
                resultados[alg][tipo][str(tamanho)]["desvio_padrao"]
                for tamanho in tamanhos
            ]

            plt.errorbar(
                tamanhos,
                medias,
                yerr=desvios,
                marker='o',
                capsize=5,
                label=alg
            )

        plt.xscale('log')

        plt.legend()
        plt.grid(True, which="both", ls="--")
        plt.savefig(f"grafico_abismo_{tipo.lower()}.png")
        plt.close()


if __name__ == "__main__":
    # Ponto de entrada do script responsável pela geração das visualizações
    # derivadas da análise empírica dos algoritmos avaliados.
    plot_charts()

    print(
        "Análise visual concluída: gráficos gerados com base na média empírica "
        "e no desvio padrão das execuções (k = 5)."
    )