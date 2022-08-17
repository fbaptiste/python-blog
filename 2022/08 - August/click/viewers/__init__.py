import click

from viewers.csv_viewer import preview_csv
from viewers.enums import TableFormat
from viewers.json_viewer import preview_json


@click.group(name="viewers")
def viewers_group():
    """CLI commands for viewing CSV and JSON files"""


@click.command(name="json")
@click.argument("file_name", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--numlines",  # this will be the argument name used in the function being decorated
    "-n",
    default=None,
    type=click.IntRange(1),
    help="Number of lines of the JSON object to display, or omit to view the entire file",
)
@click.option(
    "-i",
    "--indent",
    default=4,
    type=click.IntRange(0),
    help="Specifies the indentation level for viewing the JSON object",
)
def view_json(file_name, numlines, indent):
    """Use FILE_NAME to Specify a path to the JSON file you wish to preview"""
    result = preview_json(file_name=file_name, first_n=numlines, indent=indent)
    click.echo(result)


@click.command(name="csv")
@click.argument("file_name", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "--has-header",
    "has_headers",
    is_flag=True,
    default=False,
    help="Specify this flag is the CSV file has a header row",
)
@click.option(
    "--numlines",
    "-n",
    "line_count",
    default=None,
    type=click.IntRange(1),
    help="Number of rows to display (excluding header row, if any)",
)
@click.option(
    "--format",
    "-f",
    "format_",  # actually need this format is a Python built-in function
    default=TableFormat.fancy_outline.name,
    type=click.Choice([e.name for e in TableFormat], case_sensitive=True),
    help="Specify the formatting style",
)
def view_csv(file_name, line_count, has_headers, format_):
    """View CSV files"""
    format_ = TableFormat[format_]
    result = preview_csv(
        file_name=file_name, first_n=line_count, has_header_row=has_headers, table_format=format_
    )
    click.echo(result)


viewers_group.add_command(view_json)
viewers_group.add_command(view_csv)
