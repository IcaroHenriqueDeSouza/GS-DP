from math import inf

from dynamic_programming import (
    dp_bottom_up,
    weighted_cost
)

from brute_force import (
    brute_force_path
)

def test_weighted_cost():

    assert weighted_cost(
        10,
        0.5
    ) == 15

def test_dp_simple_grid():

    cost_grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]

    risk_grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    cost, path, _ = dp_bottom_up(
        cost_grid,
        risk_grid
    )

    assert cost == 7

    assert path[0] == (0, 0)

    assert path[-1] == (2, 2)

def test_dp_blocked_origin():

    cost_grid = [
        [-1, 1],
        [1, 1]
    ]

    risk_grid = [
        [0, 0],
        [0, 0]
    ]

    cost, path, _ = dp_bottom_up(
        cost_grid,
        risk_grid
    )

    assert cost == inf

    assert path == []

def test_dp_empty_grid():

    cost, path, dp = dp_bottom_up(
        [],
        []
    )

    assert cost == inf

    assert path == []

    assert dp == []

def test_brute_force_matches_dp():

    cost_grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]

    risk_grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]

    bf_cost, _, _ = brute_force_path(
        cost_grid,
        risk_grid
    )

    dp_cost, _, _ = dp_bottom_up(
        cost_grid,
        risk_grid
    )

    assert bf_cost == dp_cost

from scenarios import (
    generate_small_scenario
)

from monte_carlo import (
    monte_carlo_simulation
)

def test_monte_carlo():

    scenario = generate_small_scenario()

    result = monte_carlo_simulation(
        scenario,
        iterations=100
    )

    assert len(result.costs) > 0

    assert result.mean > 0