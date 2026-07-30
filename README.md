# yyc-historical-city-limits

![coding_style](https://img.shields.io/badge/code%20style-black-000000.svg)
[![GitHub Pages](https://github.com/zehengl/yyc-historical-city-limits/actions/workflows/gh-deploy.yml/badge.svg)](https://github.com/zehengl/yyc-historical-city-limits/actions/workflows/gh-deploy.yml)

A Python script that creates a video illustrating the historical changes in the city limits of Calgary

## Environment

- Python 3.12
- FFmpeg

## Getting Started

    python -m venv .venv
    .venv\Scripts\activate
    python -m pip install -U pip
    pip install -r requirements.txt
    python generate.py

> Use `pip install -r requirements-dev.txt` for development.

## Credits

- City of Calgary AcrGIS [Services Directory](https://tiles.arcgis.com/tiles/AVP60cs0Q9PEA8rH/arcgis/rest/services)
- [Historic City Limits][3] of Calgary
- [Reduce Generated GIF Size Using FFMPEG][4]

[3]: https://data.calgary.ca/Base-Maps/Historic-City-Limits/twfe-ukxx
[4]: https://superuser.com/a/1049820
