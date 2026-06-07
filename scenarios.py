# scenarios.py

from dataclasses import dataclass
import random


@dataclass
class Scenario:
    cost: list[list[int]]
    risk: list[list[float]]
    probability: list[list[float]]


def generate_satellite_grid(
    rows: int,
    cols: int,
    blocked_probability: float = 0.05,
    seed: int | None = 42
) -> Scenario:

    if seed is not None:
        random.seed(seed)

    cost_grid = []
    risk_grid = []
    probability_grid = []

    for i in range(rows):

        cost_row = []
        risk_row = []
        probability_row = []

        for j in range(cols):

            # Simulação de município inacessível
            if random.random() < blocked_probability:
                cost = -1
            else:
                cost = random.randint(5, 50)

            risk = round(random.uniform(0.0, 1.0), 2)

            probability = round(
                random.uniform(0.1, 0.9),
                2
            )

            cost_row.append(cost)
            risk_row.append(risk)
            probability_row.append(probability)

        cost_grid.append(cost_row)
        risk_grid.append(risk_row)
        probability_grid.append(probability_row)

    # Garante origem e destino acessíveis
    cost_grid[0][0] = max(cost_grid[0][0], 5)
    cost_grid[rows - 1][cols - 1] = max(
        cost_grid[rows - 1][cols - 1],
        5
    )

    return Scenario(
        cost=cost_grid,
        risk=risk_grid,
        probability=probability_grid
    )


def generate_small_scenario() -> Scenario:
    return generate_satellite_grid(
        rows=5,
        cols=5,
        blocked_probability=0.0,
        seed=42
    )


def generate_medium_scenario() -> Scenario:
    return generate_satellite_grid(
        rows=20,
        cols=20,
        blocked_probability=0.05,
        seed=42
    )


def generate_large_scenario() -> Scenario:
    return generate_satellite_grid(
        rows=50,
        cols=50,
        blocked_probability=0.08,
        seed=42
    )

def generate_random_scenario(
    size: int,
    blocked_probability: float = 0.05,
    seed: int | None = 42
) -> Scenario:
    """
    Gera uma grade quadrada NxN para benchmarks.
    """

    return generate_satellite_grid(
        rows=size,
        cols=size,
        blocked_probability=blocked_probability,
        seed=seed
    )

if __name__ == "__main__":

    scenario = generate_small_scenario()

    print("COST")
    for row in scenario.cost:
        print(row)

    print("\nRISK")
    for row in scenario.risk:
        print(row)

    print("\nPROBABILITY")
    for row in scenario.probability:
        print(row)