import os

import matplotlib.pyplot as plt


def ensure_output_dir():

    os.makedirs(
        "outputs",
        exist_ok=True
    )


# Heatmap DP
def plot_dp_heatmap(
    dp_table,
    filename="outputs/dp_heatmap.png"
):

    ensure_output_dir()

    safe_table = [
        [
            0 if value == float("inf")
            else value
            for value in row
        ]
        for row in dp_table
    ]

    plt.figure(figsize=(8, 6))

    plt.imshow(
        safe_table,
        aspect="auto"
    )

    plt.colorbar(
        label="Custo Acumulado"
    )

    plt.title(
        "Heatmap da Tabela DP"
    )

    plt.xlabel(
        "Coluna"
    )

    plt.ylabel(
        "Linha"
    )

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# Histograma Monte Carlo
def plot_monte_carlo_histogram(
    costs,
    filename="outputs/histogram.png"
):

    ensure_output_dir()

    plt.figure(figsize=(8, 6))

    plt.hist(
        costs,
        bins=30
    )

    plt.title(
        "Distribuição dos Custos"
    )

    plt.xlabel(
        "Custo"
    )

    plt.ylabel(
        "Frequência"
    )

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# Boxplot Monte Carlo
def plot_monte_carlo_boxplot(
    costs,
    filename="outputs/boxplot.png"
):

    ensure_output_dir()

    plt.figure(figsize=(8, 4))

    plt.boxplot(costs)

    plt.title(
        "Boxplot dos Custos"
    )

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# Escalabilidade
def plot_scalability(
    sizes,
    execution_times,
    filename="outputs/scalability.png"
):

    ensure_output_dir()

    plt.figure(figsize=(8, 6))

    plt.plot(
        sizes,
        execution_times,
        marker="o"
    )

    plt.title(
        "Escalabilidade da Programação Dinâmica"
    )

    plt.xlabel(
        "Tamanho da Grade"
    )

    plt.ylabel(
        "Tempo (ms)"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# Uso de memória
def plot_memory_usage(
    sizes,
    memory_usage,
    filename="outputs/memory_usage.png"
):

    ensure_output_dir()

    plt.figure(figsize=(8, 6))

    plt.plot(
        sizes,
        memory_usage,
        marker="o"
    )

    plt.title(
        "Uso de Memória"
    )

    plt.xlabel(
        "Tamanho da Grade"
    )

    plt.ylabel(
        "Memória (MB)"
    )

    plt.grid(True)

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


# Sensibilidade
def plot_sensitivity(
    labels,
    values,
    filename="outputs/sensitivity.png"
):

    ensure_output_dir()

    plt.figure(figsize=(8, 6))

    plt.bar(
        labels,
        values
    )

    plt.title(
        "Análise de Sensibilidade"
    )

    plt.ylabel(
        "Custo Médio"
    )

    plt.tight_layout()

    plt.savefig(filename)

    plt.close()


if __name__ == "__main__":

    plot_scalability(
        [5, 10, 20, 50],
        [0.07, 0.23, 0.97, 4.80]
    )

    plot_memory_usage(
        [5, 10, 20, 50],
        [0.002, 0.009, 0.032, 0.120]
    )

    plot_monte_carlo_histogram(
        [100, 110, 120, 115, 130, 125]
    )

    plot_monte_carlo_boxplot(
        [100, 110, 120, 115, 130, 125]
    )

    print(
        "Gráficos de teste gerados em outputs/"
    )