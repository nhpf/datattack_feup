import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# shp -> shapefile (geometry)
# dbf -> database (extra info)
# prj - projection
# shx - index

# Get shape of municipalities and parishes
portugal_municipalities = gpd.read_file("data_concelhos/concelhos.shp")

# Remove islands
portugal_municipalities = portugal_municipalities[portugal_municipalities.NAME_1 != "Azores"]
portugal_municipalities = portugal_municipalities[portugal_municipalities.NAME_1 != "Madeira"]

# Get point defined by user
lat, lon = 40.9800516, -8.202641
user_point = Point(lon, lat)


def get_municipality(point: Point):
    for index, row in portugal_municipalities.iterrows():
        polygon = row['geometry']
        # Check if the point is inside the polygon
        if polygon.contains(point):
            # Return the index or other properties of the polygon
            return {
                "district": row.NAME_1,
                "municipality": row.NAME_2,
                "municipality_gdf": gpd.GeoDataFrame([row], crs=portugal_municipalities.crs)
            }


def plot_point_in_map(point, municipality_gdf):
    point_df = gpd.GeoDataFrame(geometry=[point])
    pt_map = portugal_municipalities.plot()
    municipality_gdf.plot(ax=pt_map, color='yellow')
    point_df.plot(ax=pt_map, color='red', markersize=10)
    plt.axis('off')
    plt.show()


municipality_data = get_municipality(point=user_point)
plot_point_in_map(user_point, municipality_data["municipality_gdf"])

# get_municipality(user_point)

# portugal_parishes.plot(cmap="viridis")
# plt.show()

# # Create a map of the shapes in the original GeoDataFrame
# ax = portugal_municipalities.plot()
# gdf_point.plot(ax=ax, color='red', markersize=20)
#
# plt.show()

# pd.options.display.width = 100000
# pd.options.display.max_columns = 100
# print(portugal_parishes)

# data.plot()
# plt.show()


