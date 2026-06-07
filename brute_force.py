from math import inf


def weighted_cost(cost: int, risk: float) -> float:
    return cost * (1 + risk)


def brute_force_path(
    cost_grid: list[list[int]],
    risk_grid: list[list[float]]
):
    """
    Retorna:
        menor_custo
        melhor_caminho
        total_chamadas
    """

    if not cost_grid or not cost_grid[0]:
        return inf, [], 0

    rows = len(cost_grid)
    cols = len(cost_grid[0])

    recursive_calls = 0

    best_cost = inf
    best_path = []

    def dfs(
        row: int,
        col: int,
        current_cost: float,
        current_path: list
    ):
        nonlocal recursive_calls
        nonlocal best_cost
        nonlocal best_path

        recursive_calls += 1

        # célula inválida
        if row >= rows or col >= cols:
            return

        # bloqueada
        if cost_grid[row][col] == -1:
            return

        current_cost += weighted_cost(
            cost_grid[row][col],
            risk_grid[row][col]
        )

        current_path = current_path + [(row, col)]

        # destino
        if row == rows - 1 and col == cols - 1:

            if current_cost < best_cost:
                best_cost = current_cost
                best_path = current_path

            return

        # direita
        dfs(
            row,
            col + 1,
            current_cost,
            current_path
        )

        # baixo
        dfs(
            row + 1,
            col,
            current_cost,
            current_path
        )

    dfs(
        0,
        0,
        0,
        []
    )

    return (
        best_cost,
        best_path,
        recursive_calls
    )

if __name__ == "__main__":

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

    cost, path, calls = brute_force_path(
        cost_grid,
        risk_grid
    )

    print("Menor custo:", cost)
    print("Melhor caminho:", path)
    print("Chamadas:", calls)
