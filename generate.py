# %%
import io
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

import cv2
import folium
import pandas as pd
import requests
from bs4 import BeautifulSoup
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
services_url = "https://tiles.arcgis.com/tiles/AVP60cs0Q9PEA8rH/arcgis/rest/services"
html_doc = requests.get(services_url).content
soup = BeautifulSoup(html_doc, "html.parser")

items = soup.find_all("li")
services_list = []
for item in items:
    name = item.find("a").text
    # pattern_wmasp = re.compile(r"^Calgary_\d{4}_WMASP$")
    pattern_orthophoto_web = re.compile(r"^Calgary_Orthophoto_Web_\d{4}$")
    if pattern_orthophoto_web.match(name):
        services_list.append(name)
services_list = sorted(services_list)
services_list

# %%
size = 2048

for name in tqdm(services_list, desc="Downloading images"):
    y = int(name.split("_")[-1])
    tiles_url = f"{services_url}/{name}/MapServer/tile/{{z}}/{{y}}/{{x}}"

    m = folium.Map(
        location=(51.0447, -114.0719),
        zoom_start=12,
        tiles=tiles_url,
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

    img_data = m._to_png(5, size=[size, size])
    img = Image.open(io.BytesIO(img_data))
    img.save(output / f"year-{y}.png")

# %%
out = cv2.VideoWriter(
    str(output / f"output1.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 1, (size, size)
)

for filename in tqdm(sorted(output.glob("year-*.png")), desc="Adding frames"):
    img = cv2.imread(str(filename))
    img = cv2.putText(
        img,
        filename.stem.replace("-", " ").capitalize(),
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
    tiles_url = (
        f"{services_url}/CurrentOrthophoto_WMASP/MapServer/tile/{{z}}/{{y}}/{{x}}"
    )
    m = folium.Map(
        location=(51.0447, -114.0719),
        zoom_start=12,
        zoom_control=False,
        tiles=tiles_url,
        attr="The City of Calgary",
        width=size,
        height=size,
    )
    year = row["start_year"]
    poly = row["the_geom"]

    folium.GeoJson(
        poly,
        style_function=lambda _: {"fillColor": "#000000", "color": "#c8102e"},
    ).add_to(m)

    img_data = m._to_png(5, size=[size, size])
    img = Image.open(io.BytesIO(img_data))
    img.save(output / f"current-as-if-in-{year}.png")

# %%
out = cv2.VideoWriter(
    str(output / f"output2.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 1, (size, size)
)

for filename in tqdm(
    sorted(output.glob("current-as-if-in-*.png")), desc="Adding frames"
):
    img = cv2.imread(str(filename))
    img = cv2.putText(
        img,
        f'Calgary\'s city limit in {filename.stem.split("-")[-1]}',
        (int(size * 0.25), int(size * 0.075)),
        cv2.FONT_HERSHEY_COMPLEX,
        2,
        (46, 16, 200),
        2,
        cv2.LINE_AA,
    )
    out.write(img)

out.release()

# %%
for i in range(2):
    try:
        subprocess.call(
            f"ffmpeg -y -i output/output{i+1}.mp4 -vf palettegen output/palette{i+1}.png".split()
        )
    except:
        pass

    try:
        subprocess.call(
            f"ffmpeg -y -i output/output{i+1}.mp4 -i output/palette{i+1}.png -filter_complex paletteuse -r 10 -s 640x640 output/output{i+1}.gif".split()
        )
    except:
        pass

# %%
for i in range(2):
    shutil.copy(output / f"output{i+1}.gif", "docs")

# %%
