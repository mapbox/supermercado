import click, json
import cligj
from supermercado import edge_finder, uniontiles, burntiles, super_utils


@click.group('supermercado')
def cli():
    pass

@click.command('edges')
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

cli.add_command(edges)

@click.command('union')
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

cli.add_command(union)


@click.command('burn')
@cligj.features_in_arg
@cligj.sequence_opt
@click.argument('zoom', type=int)
def burn(features, sequence, zoom):
    """
    Burn a stream of GeoJSONs into a output stream of the tiles they intersect for a given zoom.
    """
    features = [f for f in super_utils.filter_polygons(features)]

    tiles = burntiles.burn(features, zoom)
    for t in tiles:
        click.echo(t.tolist())


cli.add_command(burn)