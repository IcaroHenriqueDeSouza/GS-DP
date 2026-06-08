from math import inf


def weighted_cost(cost: float, risk: float) -> float:
    return cost * (1 + risk)


def brute_force_path(
    cost_grid: list[list[float]],
    risk_grid: list[list[float]],
    valid_cells: int 
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

    target_idx = valid_cells - 1
    dest_row = target_idx // cols
    dest_col = target_idx % cols

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

        if row >= rows or col >= cols:
            return


        if cost_grid[row][col] == -1 or cost_grid[row][col] == inf:
            return

   
        current_cost += weighted_cost(
            cost_grid[row][col],
            risk_grid[row][col]
        )


        if current_cost >= best_cost:
            return

        new_path = current_path + [(row, col)]

  
        if row == dest_row and col == dest_col:
            if current_cost < best_cost:
                best_cost = current_cost
                best_path = new_path
            return


        dfs(row, col + 1, current_cost, new_path)


        dfs(row + 1, col, current_cost, new_path)

 
    dfs(0, 0, 0.0, [])

    return (
        best_cost,
        best_path,
        recursive_calls
    )


if __name__ == "__main__":
    from scenarios import generate_small_scenario

    scenario = generate_small_scenario()
    
    cost, path, calls = brute_force_path(
        scenario.cost,
        scenario.risk,
        scenario.valid_cells
    )
    
    print("=== Teste Local Força Bruta ===")
    print(f"Melhor Custo: {cost}")
    print(f"Caminho: {path}")
    print(f"Chamadas Recursivas: {calls}")