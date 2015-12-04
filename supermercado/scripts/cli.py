import click, json

from supermercado import edge_finder, uniontiles


@click.group('supermercado')
def cli():
    pass

@click.command('edges')
@click.argument('inputtiles', default='-', required=False)
@click.option('--parsenames', is_flag=True)
def edges(inputtiles, parsenames):
    try:
        inputtiles = click.open_file(inputtiles).readlines()
    except IOError:
        inputtiles = [inputtiles]

    # parse the input stream into an array
    tiles, zoom = edge_finder.findedges(inputtiles, parsenames)

    for t in tiles:
        click.echo(t.tolist() + [zoom])

cli.add_command(edges)

@click.command('union')
@click.argument('inputtiles', default='-', required=False)
@click.option('--parsenames', is_flag=True)
def union(inputtiles, parsenames):
    try:
        inputtiles = click.open_file(inputtiles).readlines()
    except IOError:
        inputtiles = [inputtiles]
    unioned = uniontiles.union(inputtiles, parsenames)
    for u in unioned:
        click.echo(json.dumps(u))

cli.add_command(union)