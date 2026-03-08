import time          # Módulo utilizado para aferição de tempo de execução com alta precisão (wall-clock time via perf_counter).
import json          # Módulo para serialização e persistência dos dados experimentais no formato JSON.
import sys           # Módulo para interação com parâmetros do interpretador (e.g., ajuste do limite de chamadas recursivas).
import statistics    # Biblioteca para cômputo das métricas estatísticas descritivas (média e desvio padrão amostral).
import os            # Fornece rotinas para interação com o sistema operacional, especialmente manipulação de diretórios.
import shutil        # Utilizado para operações de alto nível no sistema de arquivos, como cópia e preservação de metadados.
from datetime import datetime       # Necessário para a geração de marcas de tempo (timestamps) no versionamento dos logs.

# Importação das implementações dos algoritmos de ordenação avaliados neste estudo.
from sorting_algorithms import *
# Importação dos métodos geradores de instâncias de teste (conjuntos de dados com variadas distribuições e tamanhos).
from data_generation import *

# Função responsável por realizar o backup de resultados e artefatos de execuções anteriores,
# garantindo a preservação do histórico experimental e evitando a perda de dados por sobrescrita.
def backup_resultados_anteriores():
    # Determinação dos caminhos absolutos do diretório atual e do diretório raiz do projeto.
    dir_principal = os.path.dirname(os.path.abspath(__file__))
    dir_raiz = os.path.dirname(dir_principal)
    
    # Definição do caminho para o diretório de versionamento de resultados.
    dir_backup = os.path.join(dir_raiz, "Backup_Python")
    
    # Criação do diretório de backup caso não exista na hierarquia de arquivos.
    if not os.path.exists(dir_backup):
        os.makedirs(dir_backup)
        
    # Inicialização da lista contendo os artefatos críticos que compõem os resultados do experimento.
    arquivos_alvo = ["resultados_mestrado.json", "Relatorio_Projeto1.md"]
    
    # Verificação da integridade do diretório principal antes da varredura.
    if os.path.exists(dir_principal):
        # Varredura no diretório para inclusão automática dos gráficos (arquivos .png) gerados em execuções prévias.
        for nome in os.listdir(dir_principal):
            if nome.startswith("grafico_") and nome.endswith(".png"):
                arquivos_alvo.append(nome)
                
    # Filtragem dos artefatos: seleciona exclusivamente os arquivos que de fato existem no diretório atual.
    arquivos_existentes = [f for f in list(set(arquivos_alvo)) if os.path.exists(os.path.join(dir_principal, f))]
    
    # Executa a rotina de cópia de segurança caso haja dados prévios a serem preservados.
    if arquivos_existentes:
        # Geração de identificador único baseado no timestamp atual.
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pasta_dest = os.path.join(dir_backup, f"Execucao_{timestamp}")
        
        # Criação do subdiretório específico para a iteração histórica.
        os.makedirs(pasta_dest)
        
        # Iteração sobre os artefatos para a realização da cópia.
        for arquivo in arquivos_existentes:
            caminho_origem = os.path.join(dir_principal, arquivo)
            caminho_dest = os.path.join(pasta_dest, arquivo)
            
            # Cópia do arquivo preservando seus metadados originais (permissões, datas de criação/modificação).
            shutil.copy2(caminho_origem, caminho_dest)
        
        # Confirmação da operação no console via saída padrão (stdout).
        print(f"[*] Backup da execução anterior salvo no diretório: Backup_Python\\Execucao_{timestamp}\n")

# Ponto de entrada do sistema. Orquestra a execução do benchmark dos algoritmos de ordenação.
def main():
    # Preservação do histórico de dados prévio antes da inicialização do novo experimento.
    backup_resultados_anteriores()
    
    # Dicionário de mapeamento: associa rótulos descritivos às referências das funções dos algoritmos.
    algoritmos = {
        "Bubble Sort Padrão": bubble_sort_padrao,
        "Bubble Sort": bubble_sort,
        "Selection Sort": selection_sort,
        "Insertion Sort": insertion_sort,
        "Merge Sort": merge_sort,
        "Quick Sort": quick_sort
    }

    # Definição das dimensões dos vetores (tamanho da entrada $N$) a serem submetidos ao teste de desempenho.
    tamanhos = [1000, 10000, 100000]
    
    # Definição do tamanho amostral ($k$). A execução de múltiplas iterações independentes mitiga 
    # variações espúrias introduzidas pelo escalonador do SO e garante validade estatística aos resultados.
    K_AMOSTRAS = 5 

    # Dicionário que mapeia as distribuições iniciais dos dados de entrada aos seus respectivos métodos geradores.
    tipos_vetor = {
        "Aleatório": generate_random_array,
        "Crescente": generate_sorted_array,
        "Decrescente": generate_reverse_sorted_array
    }

    # Inicialização declarativa da estrutura de dados aninhada via dictionary comprehension.
    # Armazenará as métricas descritivas estruturadas por: Algoritmo -> Distribuição -> Tamanho -> Métricas.
    resultados = {nome_alg: {tipo: {str(tamanho): {"media": 0, "desvio_padrao": 0} for tamanho in tamanhos} for tipo in tipos_vetor} for nome_alg in algoritmos}

    print(f"Iniciando o protocolo de benchmarking com tamanho amostral estipulado em $k={K_AMOSTRAS}$.")

    # Iteração sobre os diferentes tamanhos de entrada (complexidade espacial escalar).
    for tamanho in tamanhos:
        print(f"\n{'='*40}\n--- Dimensão do vetor ($N$): {tamanho} ---\n{'='*40}")
        
        # Iteração sobre os diferentes cenários de ordenação prévia dos dados (distribuições).
        for tipo, func_geradora in tipos_vetor.items():
            print(f"\nDistribuição: {tipo} | Instanciando {K_AMOSTRAS} vetores amostrais...")
            
            # Geração das $k$ instâncias do problema.
            # Esta etapa antecede a cronometragem para assegurar que todos os algoritmos processem
            # estritamente o mesmo conjunto de dados, garantindo simetria experimental na avaliação comparativa.
            vetores_originais = [func_geradora(tamanho) for _ in range(K_AMOSTRAS)]
            
            # Submissão das instâncias a cada um dos algoritmos de ordenação sob análise.
            for nome_alg, func_ord in algoritmos.items():
                tempos_execucoes = []
                print(f"Avaliando {nome_alg} ({K_AMOSTRAS} iterações)...", end=" ", flush=True)

                # Coleta empírica de métricas computacionais através da execução das $k$ amostras.
                for iteracao in range(K_AMOSTRAS):
                    # Criação de cópia rasa (shallow copy) do vetor original.
                    # Necessário pois os algoritmos podem operar in-place, o que mutaria a instância
                    # e invalidaria sua reutilização para os algoritmos subsequentes.
                    vetor_teste = list(vetores_originais[iteracao]) 
                    
                    # Registro do tempo de início da execução em alta resolução.
                    inicio = time.perf_counter()
                    
                    # Invocação da rotina de ordenação sob o vetor de teste.
                    func_ord(vetor_teste)
                    
                    # Registro do tempo de término da execução.
                    fim = time.perf_counter()
                    
                    # Armazenamento do tempo total de processamento da iteração atual ($\Delta t$).
                    tempos_execucoes.append(fim - inicio)
                
                # Cômputo da média aritmética dos tempos de execução coletados empiricamente.
                media = statistics.mean(tempos_execucoes)
                
                # Cômputo do desvio padrão amostral. Aplicado condicionalmente para evitar 
                # indeterminação matemática em casos de amostra unitária ($k=1$).
                desvio = statistics.stdev(tempos_execucoes) if K_AMOSTRAS > 1 else 0.0

                # Atualização do modelo de dados com as métricas estatísticas consolidadas.
                resultados[nome_alg][tipo][str(tamanho)]["media"] = media
                resultados[nome_alg][tipo][str(tamanho)]["desvio_padrao"] = desvio
                
                # Log contínuo via saída padrão para acompanhamento progressivo da execução experimental.
                print(f"[Média: {media:.4f}s | Desvio Padrão: \pm{desvio:.4f}s]")

    # Fase final: persistência dos dados consolidados em armazenamento não-volátil.
    # Utiliza-se a codificação UTF-8 para assegurar a conformidade universal dos caracteres.
    with open('resultados_mestrado.json', 'w', encoding='utf-8') as f:
        # Serialização do dicionário para formato JSON estritamente formatado (indentado).
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    print("\nExecução do benchmarking finalizada. Artefatos de saída gerados em 'resultados_mestrado.json'.")

# Guarda de inclusão padrão da linguagem Python.
# Garante que a rotina principal (main) seja isolada e invocada exclusivamente quando 
# o script é executado como programa de entrada, prevenindo execuções colaterais durante importações de módulo.
if __name__ == "__main__":
    main()