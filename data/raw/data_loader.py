
from pathlib import Path
from dataclasses import dataclass
import math
import pandas as pd


@dataclass
class Scenario:
    cost: list[list[int]]
    risk: list[list[float]]
    probability: list[list[float]]
    valid_cells: int

def normalize(
    value,
    min_value,
    max_value
):

    if max_value == min_value:
        return 0.0

    return (
        value - min_value
    ) / (
        max_value - min_value
    )


def load_rainfall_data():

    base_dir = Path(__file__).parent

    january_path = base_dir / "data.csv"
    december_path = base_dir / "data 2.csv"

    january = pd.read_csv(
        january_path,
        sep=";"
    )

    december = pd.read_csv(
        december_path,
        sep=";"
    )

    for df in [january, december]:

        df["municipio"] = (
            df["municipio"]
            .astype(str)
            .str.strip()
            .str.upper()
        )

        df["valorMedida"] = (
            df["valorMedida"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        df["latitude"] = (
            df["latitude"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        df["longitude"] = (
            df["longitude"]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    january_mean = (
        january
        .groupby("municipio")
        .agg({
            "valorMedida": "mean",
            "latitude": "first",
            "longitude": "first"
        })
        .reset_index()
    )

    december_mean = (
        december
        .groupby("municipio")
        .agg({
            "valorMedida": "mean"
        })
        .reset_index()
    )

    jan_set = set(
        january_mean["municipio"]
    )

    dec_set = set(
        december_mean["municipio"]
    )

    
    print(
        sorted(
            jan_set - dec_set
        )
    )

    
    print(
        sorted(
            dec_set - jan_set
        )
    )

    merged = january_mean.merge(
        december_mean,
        on="municipio",
        how="outer",
        suffixes=(
            "_jan",
            "_dec"
        )
    )

    merged["valorMedida_jan"] = (
        merged["valorMedida_jan"]
        .fillna(
            january_mean["valorMedida"].mean()
        )
    )

    merged["valorMedida_dec"] = (
        merged["valorMedida_dec"]
        .fillna(
            december_mean["valorMedida"].mean()
        )
    )

    

    print(f"Municípios processados:{len(merged)}")
    
    
    merged["rainfall_mean"] = (
        merged["valorMedida_jan"]
        + merged["valorMedida_dec"]
    ) / 2

    merged["variation"] = (
        merged["valorMedida_jan"]
        - merged["valorMedida_dec"]
    ).abs()

    return merged


def build_geospatial_grid():

    data = load_rainfall_data()

    rainfall_min = (
        data["rainfall_mean"]
        .min()
    )

    rainfall_max = (
        data["rainfall_mean"]
        .max()
    )

    variation_min = (
        data["variation"]
        .min()
    )

    variation_max = (
        data["variation"]
        .max()
    )

    municipalities = []
    valid_cells = len(municipalities)
    
    for _, row in data.iterrows():

        rainfall_norm = normalize(
            row["rainfall_mean"],
            rainfall_min,
            rainfall_max
    )

        variation_norm = normalize(
            row["variation"],
            variation_min,
            variation_max
    )

        cost = int(
            10
            + rainfall_norm * 40
        )

        risk = float(
            round(
                variation_norm,
                2
            )
        )

        probability = float(
            round(
                0.20 + variation_norm * 0.75,
                2
            )
        )

        municipalities.append({
            "municipio": row["municipio"],
            "latitude": row["latitude"],
            "longitude": row["longitude"],
            "cost": cost,
            "risk": risk,
            "probability": probability
        })

    municipalities.sort(
        key=lambda x: (
            x["latitude"],
            x["longitude"]
        )
    )
    print(
    "\nQuantidade de municípios:",
    len(municipalities)
)
    
    grid_size = math.ceil(
    math.sqrt(
        len(municipalities)
    )
)
    
    print(f"Tamanho da grade: {grid_size}x{grid_size}")

    
    cost_grid = []
    risk_grid = []
    probability_grid = []

    index = 0

    for _ in range(grid_size):

        cost_row = []
        risk_row = []
        probability_row = []

        for _ in range(grid_size):

            if index < len(municipalities):

                municipality = municipalities[
                    index
                ]

                cost_row.append(
                    municipality["cost"]
                )

                risk_row.append(
                    municipality["risk"]
                )

                probability_row.append(
                    municipality["probability"]
                )

            else:

                cost_row.append(-1)
                risk_row.append(0.0)
                probability_row.append(0.0)

            index += 1

        cost_grid.append(cost_row)
        risk_grid.append(risk_row)
        probability_grid.append(
            probability_row
        )

    return Scenario(
        cost=cost_grid,
        risk=risk_grid,
        probability=probability_grid,
        valid_cells=len(municipalities)
    )


if __name__ == "__main__":

    scenario = build_geospatial_grid()

    print("\nCOST GRID\n")

    for row in scenario.cost:
        print(row)

    print("\nRISK GRID\n")

    for row in scenario.risk:
        print(row)

    print("\nPROBABILITY GRID\n")

    for row in scenario.probability:
        print(row)
