from dynamic_programming import (
    dp_bottom_up
)

from monte_carlo import (
    monte_carlo_simulation
)

from performance_monitor import (
    benchmark_algorithm
)

from scenarios import (
    generate_small_scenario,
    generate_random_scenario
)

from visualizations import (
    plot_dp_heatmap,
    plot_monte_carlo_histogram,
    plot_monte_carlo_boxplot,
    plot_scalability,
    plot_memory_usage
)


def generate_dp_reports():

    scenario = generate_small_scenario()

    _, _, dp_table = dp_bottom_up(
        scenario.cost,
        scenario.risk
    )

    plot_dp_heatmap(
        dp_table
    )

    print(
        "✓ Heatmap DP gerado"
    )


def generate_monte_carlo_reports():

    scenario = generate_small_scenario()

    result = monte_carlo_simulation(
        scenario,
        iterations=1000
    )

    plot_monte_carlo_histogram(
        result.costs
    )

    plot_monte_carlo_boxplot(
        result.costs
    )

    print(
        "✓ Relatórios Monte Carlo gerados"
    )


def generate_benchmark_reports():

    benchmark = benchmark_algorithm(
        algorithm=dp_bottom_up,
        scenario_generator=generate_random_scenario,
        sizes=[5, 10, 20, 30, 40, 50]
    )

    plot_scalability(
        benchmark.sizes,
        benchmark.execution_times
    )

    plot_memory_usage(
        benchmark.sizes,
        benchmark.memory_usage
    )

    print(
        "✓ Relatórios de benchmark gerados"
    )


def main():

    print(
        "\nGerando relatórios...\n"
    )

    generate_dp_reports()

    generate_monte_carlo_reports()

    generate_benchmark_reports()

    print(
        "\nTodos os relatórios foram gerados."
    )

    print(
        "Verifique a pasta outputs/"
    )


if __name__ == "__main__":

    main()