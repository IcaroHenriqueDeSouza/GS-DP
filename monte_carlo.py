from dataclasses import dataclass
import numpy as np

from dynamic_programming import dp_bottom_up


@dataclass
class MonteCarloResult:
    costs: list[float]

    mean: float
    median: float
    std: float

    ci_lower: float
    ci_upper: float


def sample_probability(probability: float) -> float:
    """
    Gera uma amostra baseada na probabilidade histórica.
    """

    alpha = max(
        probability * 10,
        0.1
    )

    beta = max(
        (1 - probability) * 10,
        0.1
    )

    return np.random.beta(
        alpha,
        beta
    )


def monte_carlo_simulation(
    scenario,
    iterations: int = 10000
) -> MonteCarloResult:
    """
    Executa simulações Monte Carlo utilizando
    as probabilidades históricas do cenário.
    """

    simulated_costs = []

    for _ in range(iterations):

        simulated_risk = []

        for i in range(len(scenario.risk)):

            row = []

            for j in range(len(scenario.risk[0])):

                factor = sample_probability(
                    scenario.probability[i][j]
                )

                row.append(
                    scenario.risk[i][j] * factor
                )

            simulated_risk.append(row)

        cost, _, _ = dp_bottom_up(
            scenario.cost,
            simulated_risk
        )

        if cost != float("inf"):
            simulated_costs.append(cost)

    if not simulated_costs:
        raise ValueError(
            "Nenhum caminho válido foi encontrado durante a simulação."
        )

    costs = np.array(simulated_costs)

    mean = float(np.mean(costs))
    median = float(np.median(costs))
    std = float(np.std(costs))

    margin = (
        1.96
        * std
        / np.sqrt(len(costs))
    )

    return MonteCarloResult(
        costs=simulated_costs,
        mean=mean,
        median=median,
        std=std,
        ci_lower=mean - margin,
        ci_upper=mean + margin
    )