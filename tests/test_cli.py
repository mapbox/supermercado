import json
import os

import mercantile
from click.testing import CliRunner
from supermercado.scripts.cli import cli


def test_union_cli():
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/union.txt')
    expectedFilename = os.path.join(os.path.dirname(__file__), 'expected/union.txt')
    runner = CliRunner()
    result = runner.invoke(cli, ['union', filename])
    assert result.exit_code == 0
    with open(expectedFilename) as ofile:
        expected = ofile.readlines()
    # TODO fuzzy test of featurecollection equality
    assert len(result.output.strip().split("\n")) == len(expected)


def test_edge_cli():
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/edges.txt')
    expectedFilename = os.path.join(os.path.dirname(__file__), 'expected/edges.txt')
    runner = CliRunner()
    result = runner.invoke(cli, ['edges', filename])
    assert result.exit_code == 0
    with open(expectedFilename) as ofile:
        expected = ofile.read()
    assert result.output == expected

def test_burn_cli():
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/shape.geojson')
    expectedFilename = os.path.join(os.path.dirname(__file__), 'expected/burned.txt')

    with open(filename) as ofile:
        geojson = ofile.read()

    runner = CliRunner()
    result = runner.invoke(cli, ['burn', '9'], input=geojson)
    assert result.exit_code == 0

    with open(expectedFilename) as ofile:
        expected = ofile.read()
    assert result.output == expected


def test_burn_tile_center_point_roundtrip():
    tile = [83885, 202615, 19]
    w, s, e, n = mercantile.bounds(*tile)

    x = (e - w) / 2 + w
    y = (n - s) / 2 + s

    point_feature = {
        "type": "Feature",
        "properties": {},
        "geometry": {"type": "Point", "coordinates": [x, y]}
    }

    runner = CliRunner()
    result = runner.invoke(cli, ["burn", "19"], input=json.dumps(point_feature))

    assert json.loads(result.output) == tile


def test_burn_tile_center_lines_roundtrip():
    tiles = list(mercantile.children([0, 0, 0]))
    bounds = (mercantile.bounds(*t) for t in tiles)
    coords = (((e - w) / 2 + w, (n - s) / 2 + s) for w, s, e, n in bounds)

    features = {
        "type": "Feature",
        "properties": {},
        "geometry": {"type": "LineString", "coordinates": list(coords)}
    }


    runner = CliRunner()
    result = runner.invoke(cli, ["burn", "1"], input=json.dumps(features))

    output_tiles = [json.loads(t) for t in result.output.split("\n") if t]
    assert sorted(output_tiles) == sorted([list(t) for t in tiles])


def test_burn_cli_tile_shape():
    tilegeom = '{"bbox": [-122.4755859375, 37.75334401310657, -122.431640625, 37.78808138412046], "geometry": {"coordinates": [[[-122.4755859375, 37.75334401310657], [-122.4755859375, 37.78808138412046], [-122.431640625, 37.78808138412046], [-122.431640625, 37.75334401310657], [-122.4755859375, 37.75334401310657]]], "type": "Polygon"}, "id": "(1309, 3166, 13)", "properties": {"title": "XYZ tile (1309, 3166, 13)"}, "type": "Feature"}'
    runner = CliRunner()
    result = runner.invoke(cli, ['burn', '13'], input=tilegeom)

    assert result.output == '[1309, 3166, 13]\n'
