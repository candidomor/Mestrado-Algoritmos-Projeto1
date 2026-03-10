import json
import os
import matplotlib.pyplot as plt
import numpy as np

# Configurações de diretórios
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir = os.path.dirname(os.path.abspath(__file__))

# Arquivos de resultados de cada linguagem
arquivos = {
    "Python": os.path.join(base_dir, "Principal", "resultados_mestrado.json"),
    "C#": os.path.join(base_dir, "CSharp_Benchmark", "resultados_csharp.json"),
    "C++": os.path.join(base_dir, "Cpp_Benchmark", "resultados_cpp.json"),
    "Rust": os.path.join(base_dir, "Rust_Benchmark", "resultados_rust.json"),
    "Java": os.path.join(base_dir, "Java_Benchmark", "resultados_java.json")
}

algoritmos = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort"]
ordens = ["Aleatório", "Crescente", "Decrescente"]
tamanhos = ["1000", "10000", "100000"]
linguagens = list(arquivos.keys())

# Carregar dados
dados = {lang: {} for lang in linguagens}
for lang, filepath in arquivos.items():
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            dados[lang] = json.load(f)
    else:
        print(f"Aviso: Arquivo {filepath} não encontrado.")

# Gerar gráficos separados para cada algoritmo
for alg in algoritmos:
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle(f"Comparação de Desempenho: {alg}", fontsize=16)

    for i, ordem in enumerate(ordens):
        ax = axes[i]
        
        x = np.arange(len(tamanhos))  # posições dos tamanhos no eixo x
        width = 0.15  # largura das barras
        
        for j, lang in enumerate(linguagens):
            tempos = []
            for tam in tamanhos:
                try:
                    tempo = dados[lang][alg][ordem][tam]['media']
                except KeyError:
                    tempo = 0
                tempos.append(tempo)
            
            # Posição da barra para a linguagem atual
            pos = x - (len(linguagens) * width) / 2 + j * width + width/2
            
            # Barras normais, depois aplicamos log no eixo y
            ax.bar(pos, tempos, width, label=lang)
        
        ax.set_title(f"Arranjo {ordem}")
        ax.set_xlabel("Tamanho do Arranjo")
        ax.set_ylabel("Tempo (s) - Escala Log")
        ax.set_xticks(x)
        ax.set_xticklabels(tamanhos)
        ax.set_yscale('log')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adicionar legenda apenas no último subplot para não poluir
    axes[-1].legend(title="Linguagens", bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout(rect=[0, 0, 0.9, 0.95])  # Ajusta o layout para acomodar legenda global
    
    salvar_em = os.path.join(output_dir, f"comparacao_{alg.replace(' ', '_').lower()}.png")
    plt.savefig(salvar_em, bbox_inches='tight')
    plt.close()

print("Gráficos gerados com sucesso na pasta Extra_Multi.")
