# %%
import io
from datetime import datetime
from pathlib import Path

import cv2
import folium
import pandas as pd
import requests
from PIL import Image
from shapely.geometry import shape
from tqdm.auto import tqdm

output = Path("output")
output.mkdir(exist_ok=True)


df = pd.DataFrame(
    requests.get("https://data.calgary.ca/resource/twfe-ukxx.json").json()
)
df["the_geom"] = df["the_geom"].apply(shape)
df["end_year"] = pd.to_numeric(df["end_year"]).fillna(datetime.now().year)
df["start_year"] = pd.to_numeric(df["start_year"])
df


# %%
orthophoto_years = [
    2004,
    2006,
    2007,
    2009,
    2019,
    2021,
]

wmasp_years = [
    1997,
    1999,
    2001,
    2003,
    2005,
    2008,
    2010,
    2011,
    2012,
    2014,
    2015,
    2018,
    2020,
    2022,
]

size = 2048

for y in tqdm(orthophoto_years + wmasp_years):
    if y in orthophoto_years:
        base_url = f"https://tiles.arcgis.com/tiles/AVP60cs0Q9PEA8rH/arcgis/rest/services/Calgary_{y}_Orthophoto/MapServer/tile"
    else:
        base_url = f"https://tiles.arcgis.com/tiles/AVP60cs0Q9PEA8rH/arcgis/rest/services/Calgary_{y}_WMASP/MapServer/tile"
    m = folium.Map(
        location=(51.0447, -114.0719),
        zoom_start=12,
        tiles=base_url + "/{z}/{y}/{x}",
        attr="The City of Calgary",
        width=size,
        height=size,
        zoom_control=False,
    )

    poly = df["the_geom"][(df["start_year"] <= y) & (df["end_year"] >= y)]
    if poly.empty:
        poly = df["the_geom"][(df["end_year"] <= y)].iloc[-1]
    else:
        poly = poly.iloc[0]

    folium.GeoJson(
        poly,
        style_function=lambda _: {"fillColor": "#000000", "color": "#c8102e"},
    ).add_to(m)

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save(output / f"{y}.png")

# %%
out = cv2.VideoWriter(
    str(output / f"output.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 1, (size, size)
)

for filename in tqdm(output.glob("*.png")):
    img = cv2.imread(str(filename))
    img = cv2.putText(
        img,
        filename.stem,
        (int(size * 0.4), int(size * 0.35)),
        cv2.FONT_HERSHEY_COMPLEX,
        2,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    out.write(img)

out.release()

# %%
for row in tqdm(df.to_dict("records")):
    base_url = "https://tiles.arcgis.com/tiles/AVP60cs0Q9PEA8rH/arcgis/rest/services/CurrentOrthophoto_WMASP/MapServer/tile"
    m = folium.Map(
        location=(51.0447, -114.0719),
        zoom_start=12,
        tiles=base_url + "/{z}/{y}/{x}",
        attr="The City of Calgary",
        width=size,
        height=size,
        zoom_control=False,
    )
    year = row["start_year"]
    poly = row["the_geom"]

    folium.GeoJson(
        poly,
        style_function=lambda _: {"fillColor": "#000000", "color": "#c8102e"},
    ).add_to(m)

    img_data = m._to_png(5)
    img = Image.open(io.BytesIO(img_data))
    img.save(output / f"current-as-if-in-{year}.png")

# %%
out = cv2.VideoWriter(
    str(output / f"output2.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 1, (size, size)
)

for filename in tqdm(output.glob("current-as-if-in-*.png")):
    img = cv2.imread(str(filename))
    img = cv2.putText(
        img,
        f'Calgary\'s city limit in {filename.stem.split("-")[-1]}',
        (int(size * 0.05), int(size * 0.075)),
        cv2.FONT_HERSHEY_COMPLEX,
        2,
        (46, 16, 200),
        2,
        cv2.LINE_AA,
    )
    out.write(img)

out.release()

# %%
