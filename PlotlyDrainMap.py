#import libraries
import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#read shapefile and convert it to a geodataframe
shapefile_path = r"C:\Users\jsasser\Desktop\TestDrains\DrainsForPlotly.shp"
gdf = gpd.read_file(shapefile_path)


#sets the CRS to web mercator
if gdf.crs != "EPSG:4326":
    gdf = gdf.to_crs("EPSG:4326")
line_data = []
#Breaks the multilinestrings into a format plotly can parse
for _, row in gdf.iterrows():
    geometry = row.geometry
    attributes = row.drop("geometry").to_dict()  # Extract all attributes except geometry
    if geometry.geom_type == "LineString":
        # Extract coordinates for a single LineString
        coords = list(geometry.coords)
        for coord in coords:
            line_data.append({"lat": coord[1], "lon": coord[0], **attributes})
        line_data.append({"lat": None, "lon": None, **attributes})  # Separator
    elif geometry.geom_type == "MultiLineString":
        # Extract coordinates for each LineString in the MultiLineString
        for line in geometry.geoms:
            coords = list(line.coords)
            for coord in coords:
                line_data.append({"lat": coord[1], "lon": coord[0], **attributes})
            line_data.append({"lat": None, "lon": None, **attributes})  # Separator

#create a dataframe based on the line_data
df = pd.DataFrame(line_data)

#find the center of the map based on average of max and min lat and lon
min_lat, max_lat = df["lat"].min(), df["lat"].max()
min_lon, max_lon = df["lon"].min(), df["lon"].max()

center_lat = (min_lat + max_lat) / 2
center_lon = (min_lon + max_lon) / 2

#Create a color map dictionary based on the estabslished styling
color_map = {
    "Maintained Tile": '#FF0000',
    "Retention Pond": '#00C5FF',
    "Detention Pond": '#73DFFF',
    "Maintained Open Ditch": '#004DA8',
    "Maintained Concrete Swale": "#4CE600",
    "Maintained Grass Swale": "#4CE600",
    "Regulated Not Maintained Tile": "#FFD37F",
    "Regulated Not Maintained Open Ditch": "#002673",
    "Private Drain Relocation": "#C500FF",
    "Private Open Ditch": "#4C0073",
    "Private Tile": "#FFBEBE",
    "Vacated Tile": "#FFFFBE",
    "Pipeline": "#00E6A9",
    "Pond": "#BFD9F2"
}
#Establish line_map based on the dataframe
fig = px.line_map(
    df,
    lat="lat",
    lon="lon",
    color="Layer",
    color_discrete_map=color_map,
    hover_name="Drain_Name",
    hover_data={"lat":False, "lon": False},
    title="Tippecanoe County Regulated Drains",
    zoom=9.8,
    center={"lat": center_lat, "lon": center_lon}
)

#Format title
fig.update_layout(
    title={
        'text': 'Tippecanoe County Regulated Drains',  # The title text
        'x': 0.45,  # Center the title horizontally
        'xanchor': 'center',  # Anchor title to the center
        'y': 0.97,  # Position the title slightly below the top
        'yanchor': 'top',  # Anchor title to the top of the figure
        'font': {
            'family': 'Corbel',  # Font family
            'size': 60,  # Font size in pixels
            'color': '#860361',  # Font color
        },
        'font_shadow': 'auto'
    }
)
#Format legend
fig.update_layout(
    legend=dict(
        title="Drain Type",
        bgcolor="#29797C",  # Set the background color
        bordercolor="black",  # Optional: set border color for the legend
        borderwidth=2,
        font_family="Corbel",
        font_color="#23191A",
    )
)
#Set a basemap
fig.update_layout(
    map_style="satellite"
)
#Set the hover label styling
fig.update_layout(
    hoverlabel=dict(
        bgcolor="#29797C",
        font_size=16,
        font_family="Corbel",
        bordercolor="black"
    )
)

#Formate background color
fig.update_layout(
    paper_bgcolor='#FFFFFF',
)

fig.show(config={"responsive": True})

#Plots figure

#Writes the figure to a html file - change where this points
#fig.write_html(r"C:\Users\jsasser\Desktop\PlotlyHTML\index.html")
