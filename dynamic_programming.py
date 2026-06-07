from math import inf


def weighted_cost(cost: int, risk: float) -> float:
    
    return cost * (1 + risk)


def reconstruct_path(
    parent: list,
    row: int,
    col: int
) -> list:
    

    path = []
    current = (row, col)

    while current is not None:
        path.append(current)

        row, col = current
        current = parent[row][col]

    path.reverse()
    return path


def dp_bottom_up(
    cost_grid: list[list[int]],
    risk_grid: list[list[float]]
):
    """
    Retorna:
        custo_otimo
        caminho_otimo
        tabela_dp
    """

    if not cost_grid or not cost_grid[0]:
        return inf, [], []

    rows = len(cost_grid)
    cols = len(cost_grid[0])

    dp = [
        [inf for _ in range(cols)]
        for _ in range(rows)
    ]

    parent = [
        [None for _ in range(cols)]
        for _ in range(rows)
    ]

    # Origem bloqueada
    if cost_grid[0][0] == -1:
        return inf, [], dp

    dp[0][0] = weighted_cost(
        cost_grid[0][0],
        risk_grid[0][0]
    )

    for i in range(rows):
        for j in range(cols):

            if i == 0 and j == 0:
                continue

            # Célula bloqueada
            if cost_grid[i][j] == -1:
                continue

            current_cost = weighted_cost(
                cost_grid[i][j],
                risk_grid[i][j]
            )

            # Movimento vindo de cima
            if i > 0 and dp[i - 1][j] != inf:

                candidate = (
                    dp[i - 1][j]
                    + current_cost
                )

                if candidate < dp[i][j]:

                    dp[i][j] = candidate

                    parent[i][j] = (
                        i - 1,
                        j
                    )

            # Movimento vindo da esquerda
            if j > 0 and dp[i][j - 1] != inf:

                candidate = (
                    dp[i][j - 1]
                    + current_cost
                )

                if candidate < dp[i][j]:

                    dp[i][j] = candidate

                    parent[i][j] = (
                        i,
                        j - 1
                    )

    # Destino inalcançável
    if dp[rows - 1][cols - 1] == inf:
        return inf, [], dp

    path = reconstruct_path(
        parent,
        rows - 1,
        cols - 1
    )

    return (
        dp[rows - 1][cols - 1],
        path,
        dp
    )


if __name__ == "__main__":

    cost_grid = [
        [1, 3, 1],
        [1, 5, 1],
        [4, 2, 1]
    ]

    risk_grid = [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ]

    cost, path, dp_table = dp_bottom_up(
        cost_grid,
        risk_grid
    )

    print("Custo ótimo:", cost)
    print("Caminho:", path)

    print("\nTabela DP:")
    for row in dp_table:
        print(row)