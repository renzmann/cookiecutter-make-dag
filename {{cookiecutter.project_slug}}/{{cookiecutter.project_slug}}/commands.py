from pathlib import Path

import click
import jinja2

from ._project import get_config, get_connection


@click.group()
@click.help_option("-h", "--help")
def cli():
    pass


@cli.command()
@click.argument("file")
def ctas(file: str) -> None:
    """
    Create a new table in the analysis database using the query in FILE.
    """
    path = Path(file)
    config = get_config()

    jinja_loader = jinja2.FileSystemLoader(path.parent)
    jinja_environment = jinja2.Environment(loader=jinja_loader)
    template = jinja_environment.get_template(str(path.name))

    sql = f"""
        DROP TABLE IF EXISTS {path.stem};
        CREATE TABLE {path.stem} AS {template.render(**config)};
    """

    with get_connection() as con:
        con.executescript(sql)

