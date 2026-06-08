import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.raw.data_loader import build_geospatial_grid
from dynamic_programming import dp_bottom_up


def main():

    print("\nCarregando dados pluviométricos...\n")

    scenario = build_geospatial_grid()

    print("\nExecutando Programação Dinâmica...\n")
    cost, path, dp_table = dp_bottom_up(
        scenario.cost,
        scenario.risk,
        scenario.valid_cells
    )

    print("=" * 50)
    if isinstance(cost, float) and cost == float('inf'):
        print("Custo ótimo encontrado: Inalcançável (inf)")
    else:
        print(f"Custo ótimo encontrado: {cost:.2f}")

    print(f"Quantidade de passos: {len(path)}")

    print("\nCaminho ótimo:")
    for position in path:
        print(position)

    print("\nTabela DP:")
    for row in dp_table:
        print([round(x, 1) if x != float('inf') else "--" for x in row])

    print("=" * 50)
    print("\nGRADE DE CUSTOS\n")

    for row in scenario.cost:
        print(row)
        
    valid_index = scenario.valid_cells - 1
    target_row = valid_index // len(scenario.cost[0])
    target_col = valid_index % len(scenario.cost[0])
    print(f"\nDestino real: ({target_row}, {target_col})")
    print("=" * 50)


if __name__ == "__main__":
    main()