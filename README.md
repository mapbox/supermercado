[![PyPI](https://img.shields.io/pypi/v/supermercado.svg)](https://pypi.org/project/supermercado/) [![Tests](https://github.com/mapbox/supermercado/actions/workflows/tests.yml/badge.svg)](https://github.com/mapbox/supermercado/actions/workflows/tests.yml)

# supermercado

`supermercado` extends the functionality of [`mercantile`](https://github.com/mapbox/mercantile) with additional commands


## Quickstart

```sh
pip install supermercado
```

### Usage

```sh
Usage: supermercado [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  burn   Burn a stream of GeoJSON into a output...
  edges  For a stream of [<x>, <y>, <z>] tiles, return...
  union  Returns the unioned shape of a stream of...
```

#### `supermercado burn`

```
<{geojson} stream> | supermercado burn <zoom> | <[x, y, z] stream>
```

Takes an input stream of GeoJSON and returns a stream of intersecting `[x, y, z]`s for a given zoom.

![image](https://cloud.githubusercontent.com/assets/5084513/14003508/94bc0994-f110-11e5-8e99-e9aadf07bf8d.png)

```sh
cat data/ellada.geojson | supermercado burn 10 | mercantile shapes | fio collect
```

![image](https://cloud.githubusercontent.com/assets/5084513/14003559/d5427ba6-f110-11e5-80d5-a2aba6433e77.png)

#### `supermercado edges`
```
<[x, y, z] stream> | supermercado edges | <[x, y, z] stream>
```
Outputs a stream of `[x, y, z]`s representing the edge tiles of an input stream of `[x, y, z]`s. Edge tile = any tile that is either directly adjacent to a tile that does not exist, or diagonal to an empty tile.

```
cat data/ellada.geojson | supermercado burn 10 | supermercado edges | mercantile shapes | fio collect | geojsonio
```

![image](https://cloud.githubusercontent.com/assets/5084513/14003587/01e8e370-f111-11e5-8df4-ac3ae07bbf92.png)


#### `supermercado union`

```
<[x, y, z] stream> | supermercado union | <{geojson} stream>
```

Outputs a stream of unioned GeoJSON from an input stream of `[x, y, z]`s. Like `mercantile shapes` but as an overall footprint instead of individual shapes for each tile.

```
cat data/ellada.geojson | supermercado burn 10 | supermercado union | fio collect | geojsonio
```

![image](https://cloud.githubusercontent.com/assets/5084513/14003622/365af88c-f111-11e5-8712-28f42253e270.png)


#### `getting crazy`

```
cat data/ellada.geojson | supermercado burn 12 | supermercado edges | supermercado union | fio collect | geojsonio

```

![image](https://cloud.githubusercontent.com/assets/5084513/14003951/ccfecf3c-f113-11e5-943b-94bd6eca1536.png)


## Contributing

### Developing

```sh
git clone git@github.com:mapbox/supermercado.git
cd supermercado
uv venv
source .venv/bin/activate
uv sync --all-groups
```

### Releasing

1. Within your PR, update `pyproject.toml` with the new version number
2. Once the PR is merged, pull `main` and verify the tests

```sh
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

3. Tag with the new version number and push

```sh
# ie
$ git checkout main
$ git pull
$ git tag 1.2.3
$ git push origin main 1.2.3
```

4. GitHub Actions builds the release, runs `uvx twine check`, and publishes to PyPI
using the `pypi` environment token
