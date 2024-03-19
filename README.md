<div align="center">
    <img src="https://cdn0.iconfinder.com/data/icons/small-n-flat/24/678074-map-512.png" alt="logo" height="128">
</div>

# yyc-historical-city-limits

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)

A Python script that creates a video illustrating the historical changes in the city limits of Calgary

## Environment

- Python 3.9

## Getting Started

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -U pip
    pip install -r requirements.txt
    python generate.py
    cd output
    ffmpeg -y -i output.mp4 -vf palettegen palette.png
    ffmpeg -y -i output.mp4 -i palette.png -filter_complex paletteuse -r 10 -s 640x640 output.gif

> Use `pip install -r requirements-dev.txt` for development.

## Credits

- [Logo][1] by [Paomedia][2]
- [Historic City Limits][3] of Calgary
- [Reduce Generated GIF Size Using FFMPEG][4]

[1]: https://www.iconfinder.com/icons/299050/map_icon
[2]: https://www.iconfinder.com/paomedia
[3]: https://data.calgary.ca/Base-Maps/Historic-City-Limits/twfe-ukxx
[4]: https://superuser.com/a/1049820
