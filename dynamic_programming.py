from math import inf


def weighted_cost(cost: float, risk: float) -> float:
    return cost * (1 + risk)


def reconstruct_path(parent: list, row: int, col: int) -> list:
    path = []
    current = (row, col)

    while current is not None:
        path.append(current)
        current = parent[current[0]][current[1]]

    path.reverse()
    return path


def dp_bottom_up(
    cost_grid: list[list[float]],
    risk_grid: list[list[float]],
    valid_cells: int  
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

    dp = [[inf for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    if cost_grid[0][0] == -1 or cost_grid[0][0] == inf:
        return inf, [], dp

    dp[0][0] = weighted_cost(cost_grid[0][0], risk_grid[0][0])

    for i in range(rows):
        for j in range(cols):

            if i == 0 and j == 0:
                continue

            if cost_grid[i][j] == -1 or cost_grid[i][j] == inf:
                continue

            current_cost = weighted_cost(cost_grid[i][j], risk_grid[i][j])
            if i > 0 and dp[i - 1][j] != inf:
                candidate = dp[i - 1][j] + current_cost
                if candidate < dp[i][j]:
                    dp[i][j] = candidate
                    parent[i][j] = (i - 1, j)

            # Movimento vindo da esquerda
            if j > 0 and dp[i][j - 1] != inf:
                candidate = dp[i][j - 1] + current_cost
                if candidate < dp[i][j]:
                    dp[i][j] = candidate
                    parent[i][j] = (i, j - 1)

    target_idx = valid_cells - 1
    dest_row = target_idx // cols
    dest_col = target_idx % cols

    if dp[dest_row][dest_col] == inf:
        return inf, [], dp

    path = reconstruct_path(parent, dest_row, dest_col)

    return (
        dp[dest_row][dest_col],
        path,
        dp
    )

def dp_top_down(
    cost_grid: list[list[float]],
    risk_grid: list[list[float]],
    valid_cells: int
):
    
    if not cost_grid or not cost_grid[0]:
        return inf, [], []

    rows = len(cost_grid)
    cols = len(cost_grid[0])

    memo = [[None for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    def solve(i, j):
        if i == 0 and j == 0:
            if cost_grid[0][0] == -1 or cost_grid[0][0] == inf:
                return inf
            return weighted_cost(cost_grid[0][0], risk_grid[0][0])
        
        if i < 0 or j < 0 or cost_grid[i][j] == -1 or cost_grid[i][j] == inf:
            return inf

        if memo[i][j] is not None:
            return memo[i][j]

        current_cost = weighted_cost(cost_grid[i][j], risk_grid[i][j])
        
        from_up = solve(i - 1, j)
        from_left = solve(i, j - 1)

        if from_up == inf and from_left == inf:
            memo[i][j] = inf
            return inf

        if from_up < from_left:
            memo[i][j] = from_up + current_cost
            parent[i][j] = (i - 1, j)
        else:
            memo[i][j] = from_left + current_cost
            parent[i][j] = (i, j - 1)

        return memo[i][j]

    target_idx = valid_cells - 1
    dest_row = target_idx // cols
    dest_col = target_idx % cols

    optimal_cost = solve(dest_row, dest_col)

    if optimal_cost == inf:
        return inf, [], memo

    for r in range(rows):
        for c in range(cols):
            if memo[r][c] is None:
                solve(r, c)
            if memo[r][c] is None:
                memo[r][c] = inf

    path = reconstruct_path(parent, dest_row, dest_col)
    return optimal_cost, path, memo

from data.raw.data_loader import build_geospatial_grid

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    scenario = build_geospatial_grid()

    
    cost, path, dp_table = dp_bottom_up(
        scenario.cost,
        scenario.risk,
        scenario.valid_cells
    )

    print("\n--- RESULTADO ---")
    if cost == inf:
        print("Não foi possível encontrar um caminho válido até o destino.")
    else:
        print("Custo ótimo:", round(cost, 2))
        print("Tamanho do caminho:", len(path))
        print("Caminho (Coordenadas da Matriz):", path)

    print("\nTabela DP:")
    for row in dp_table:
        print([round(x, 1) if x != inf else "--" for x in row])