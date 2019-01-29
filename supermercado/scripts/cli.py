import re
import json
import itertools

import click
import cligj
from supermercado import edge_finder, uniontiles, burntiles, super_utils


@click.group('supermercado')
def cli():
    pass


@cli.command('edges', short_help="Return edge tiles for a stream of [<x>, <y>, <z>] tiles.")
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


class zoomCustomType(click.ParamType):
    """Custom zoom type."""

    name = "zoom"

    def convert(self, value, param, ctx):
        """Validate and parse band index."""
        try:
            assert re.match(r"^[0-9]+(..[0-9]+)?$", value)
            zooms = list(map(int, value.split("..")))
            assert all(z > 0 for z in zooms)
            return min(zooms), max(zooms)

        except (AssertionError):
            raise click.ClickException(
                "zoom must be a integer or a 'min..max' string "
                "representing a zoom range, e.g. 9..12"
            )


@cli.command('burn')
@cligj.features_in_arg
@cligj.sequence_opt
@click.argument(
    'zoom',
    type=zoomCustomType()
)
def burn(features, sequence, zoom):
    """
    Burn a stream of GeoJSONs into a output stream of the tiles they intersect for a given zoom.
    """
    features = [f for f in super_utils.filter_polygons(features)]

    tiles = (
        burntiles.burn(features, zoom) for zoom in range(zoom[0], zoom[1] + 1)
    )

    for t in itertools.chain.from_iterable(tiles):
        click.echo(t.tolist())
