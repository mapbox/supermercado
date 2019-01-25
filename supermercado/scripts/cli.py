import json
import itertools

import click
import cligj
from supermercado import edge_finder, uniontiles, burntiles, super_utils


@click.group('supermercado')
def cli():
    pass


@cli.command('edges', short_help="Return egde tiles for a stream of [<x>, <y>, <z>] tiles.")
@click.argument('inputtiles', default='-', required=False)
@click.option('--parsenames', is_flag=True)
def edges(inputtiles, parsenames):
    """
    For a stream of [<x>, <y>, <z>] tiles, return only those tiles that are on the edge.
    """
    try:
        inputtiles = click.open_file(inputtiles).readlines()
    except IOError:
        inputtiles = [inputtiles]

    # parse the input stream into an array
    tiles = edge_finder.findedges(inputtiles, parsenames)

    for t in tiles:
        click.echo(t.tolist())


@cli.command('union', short_help="Returns the unioned shape of a stream of [<x>, <y>, <z>] tiles")
@click.argument('inputtiles', default='-', required=False)
@click.option('--parsenames', is_flag=True)
def union(inputtiles, parsenames):
    """
    Returns the unioned shape of a steeam of [<x>, <y>, <z>] tiles in GeoJSON.
    """
    try:
        inputtiles = click.open_file(inputtiles).readlines()
    except IOError:
        inputtiles = [inputtiles]
    unioned = uniontiles.union(inputtiles, parsenames)
    for u in unioned:
        click.echo(json.dumps(u))


@cli.command('burn')
@cligj.features_in_arg
@cligj.sequence_opt
@click.argument(
    'zoom',
    type=str
)
def burn(features, sequence, zoom):
    """
    Burn a stream of GeoJSONs into a output stream of the tiles they intersect for a given zoom.
    """
    features = [f for f in super_utils.filter_polygons(features)]

    # Resolve the minimum and maximum zoom levels for export.
    zooms = list(map(int, zoom.split('..')))
    minzoom = zooms[0]
    maxzoom = zooms[0] if len(zooms) == 1 else zooms[1]

    tiles = []
    for zoom in range(minzoom, maxzoom + 1):
        tiles.append(burntiles.burn(features, zoom))

    for t in list(itertools.chain.from_iterable(tiles)):
        click.echo(t.tolist())
