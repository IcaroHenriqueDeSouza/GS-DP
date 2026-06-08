import os
import matplotlib.pyplot as plt
import numpy as np


def ensure_output_dir():
    os.makedirs("outputs", exist_ok=True)


# Heatmap DP 
def plot_dp_heatmap(dp_table, filename="outputs/dp_heatmap.png"):
    ensure_output_dir()

    dp_matrix = np.array(dp_table, dtype=float)

    masked_matrix = np.ma.masked_invalid(dp_matrix)
    masked_matrix = np.ma.masked_where(masked_matrix == float('inf'), masked_matrix)

    plt.figure(figsize=(8, 6))

    # O 'set_bad' define a cor das células bloqueadas/vazias 
    current_cmap = plt.cm.viridis.copy()
    current_cmap.set_bad(color='lightgray')

    im = plt.imshow(
        masked_matrix,
        aspect="auto",
        cmap=current_cmap
    )

    plt.colorbar(im, label="Custo Acumulado Otimizado")

    plt.title("Heatmap da Tabela DP (Programação Dinâmica)")
    plt.xlabel("Índice da Coluna")
    plt.ylabel("Índice da Linha")

    # Adiciona os valores numéricos dentro de cada célula para facilitar a leitura no relatório
    rows, cols = dp_matrix.shape
    for i in range(rows):
        for j in range(cols):
            val = dp_matrix[i, j]
            if val != float('inf'):
                plt.text(j, i, f"{val:.1f}", ha="center", va="center", 
                         color="white" if val > np.mean(masked_matrix) else "black")
            else:
                plt.text(j, i, "inf", ha="center", va="center", color="red")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# Histograma Monte Carlo
def plot_monte_carlo_histogram(costs, filename="outputs/histogram.png"):
    ensure_output_dir()
    plt.figure(figsize=(8, 6))

    plt.hist(costs, bins=30, edgecolor="black", color="skyblue", alpha=0.7)
    
    # Adiciona linha da média observada
    plt.axvline(np.mean(costs), color="red", linestyle="dashed", linewidth=2, label=f"Média: {np.mean(costs):.2f}")

    plt.title("Distribuição dos Custos Finais (Simulação de Monte Carlo)")
    plt.xlabel("Custo Total do Caminho")
    plt.ylabel("Frequência de Ocorrência")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# Boxplot Monte Carlo
def plot_monte_carlo_boxplot(costs, filename="outputs/boxplot.png"):
    ensure_output_dir()
    plt.figure(figsize=(6, 6))

    plt.boxplot(costs, patch_artist=True, 
                boxprops=dict(facecolor="lightgreen", color="black"),
                medianprops=dict(color="red", linewidth=2))

    plt.title("Análise de Dispersão e Outliers do Custo Mínimo")
    plt.ylabel("Custo Total")
    plt.xticks([1], ["Simulações Estocásticas"])
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# Escalabilidade (Tempo de Execução)
def plot_scalability(sizes, execution_times, filename="outputs/scalability.png"):
    ensure_output_dir()
    plt.figure(figsize=(8, 6))

    plt.plot(sizes, execution_times, marker="o", color="orange", linewidth=2, label="Bottom-Up")

    plt.title("Análise de Escalabilidade Temporal (Curva Assintótica)")
    plt.xlabel("Tamanho da Grade (N x N)")
    plt.ylabel("Tempo de Execução (ms)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# Uso de memória
def plot_memory_usage(sizes, memory_usage, filename="outputs/memory_usage.png"):
    ensure_output_dir()
    plt.figure(figsize=(8, 6))

    plt.plot(sizes, memory_usage, marker="s", color="purple", linewidth=2, label="Pico de Memória")

    plt.title("Perfil de Consumo de Memória Ram")
    plt.xlabel("Tamanho da Grade (N x N)")
    plt.ylabel("Memória Alocada (MB)")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# Sensibilidade
def plot_sensitivity(labels, values, filename="outputs/sensitivity.png"):
    ensure_output_dir()
    plt.figure(figsize=(8, 6))

    bars = plt.bar(labels, values, color="teal", edgecolor="black", alpha=0.8)

    plt.title("Análise de Sensibilidade dos Parâmetros Climáticos")
    plt.xlabel("Cenários de Risco / Fatores")
    plt.ylabel("Custo Médio Impactado")
    plt.xticks(rotation=15)
    plt.grid(True, axis="y", linestyle="--", alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f"{height:.2f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()