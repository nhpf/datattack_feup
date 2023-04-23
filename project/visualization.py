import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colormaps
import matplotlib.patches as mpatches
from utils import normalize_str


# Show the most prevalent issue category in each municipality
def plot_most_prevalent_issue_by_municipality(
        clean_df: pd.DataFrame,
        category_level: int = 2
):
    issue_by_municipality = {}
    for municipality in clean_df["Concelho"].unique():
        clean_df_by_municipality = clean_df[
            clean_df["Concelho"] == municipality
        ]
        most_prevalent_issue = clean_df_by_municipality.mode()[
            f"category{category_level}"
        ][0]
        issue_by_municipality[municipality] = most_prevalent_issue

    # Declare the color map that will be used
    color_map_names = ["viridis", "plasma", "cividis"]
    base_color_map = colormaps[color_map_names[category_level - 1]].resampled(
        len(set(issue_by_municipality.values()))
    )
    color_by_issue = {
        issue_name: base_color_map.colors[idx]
        for idx, issue_name in enumerate(set(issue_by_municipality.values()))
    }

    # Get shape of municipalities and parishes
    portugal_municipalities = gpd.read_file(
        "../georeferencing/data_concelhos/concelhos.shp"
    )
    # Remove islands
    portugal_municipalities = portugal_municipalities[
        portugal_municipalities.NAME_1 != "Azores"
    ]
    portugal_municipalities = portugal_municipalities[
        portugal_municipalities.NAME_1 != "Madeira"
    ]
    # Normalize municipality name
    portugal_municipalities["NAME_2"] = (
        portugal_municipalities["NAME_2"].astype(str).apply(normalize_str)
    )

    pt_map = portugal_municipalities.plot(color="gray")

    for municipality_name, issue_name in issue_by_municipality.items():
        matching_municipalities = portugal_municipalities.query(
            f"NAME_2=='{normalize_str(municipality_name)}'"
        )
        for _, row in matching_municipalities.iterrows():
            municipality_gdf = gpd.GeoDataFrame([row], crs=portugal_municipalities.crs)
            municipality_gdf.plot(ax=pt_map, color=color_by_issue[issue_name])

    pt_map.legend(
        handles=[
            # mpatches.Patch(color="gray", label="Sem dados"),  # We have all of it!
            *[
                mpatches.Patch(color=base_color_map.colors[idx], label=issue_name)
                for idx, issue_name in enumerate(set(issue_by_municipality.values()))
            ],
        ],
        loc="lower left",
        bbox_to_anchor=(0.1, 1),
    )
    plt.axis("off")
    plt.show()
