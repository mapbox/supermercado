import os

from click.testing import CliRunner

from supermercado.scripts.cli import cli

def test_union_cli():
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/tiles.txt')
    expectedFilename = os.path.join(os.path.dirname(__file__), 'expected/unioned.txt')
    runner = CliRunner()
    result = runner.invoke(cli, ['union', filename])
    assert result.exit_code == 0
    with open(expectedFilename) as ofile:
        expected = ofile.read()
    assert result.output == expected

def test_edge_cli():
    filename = os.path.join(os.path.dirname(__file__), 'fixtures/tiles.txt')
    expectedFilename = os.path.join(os.path.dirname(__file__), 'expected/edges.txt')
    runner = CliRunner()
    result = runner.invoke(cli, ['edges', filename])
    assert result.exit_code == 0
    with open(expectedFilename) as ofile:
        expected = ofile.read()
    assert result.output == expected
