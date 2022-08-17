import click

from converters.csv_converter import convert_csv_to_json


@click.group(name="converters")
def converters_group():
    """Converter commands."""


@click.command(name="csv")
@click.option(
    "--infile",
    "-i",
    "csv_file_name",
    type=click.Path(exists=True, dir_okay=False),
    help="specifies the input CSV file",
)
@click.option(
    "--outfile",
    "-o",
    "out_file_name",
    type=click.Path(exists=False, dir_okay=False, writable=True),
    help="specifies an output file - note that if the file exists, it will be overwritten",
)
@click.option(
    "--has-headers",
    is_flag=True,
    default=False,
    help="provide this flag to indicate the CSV file has a headers row",
)
@click.option(
    "--columns",
    "-c",
    "custom_headers",
    default=None,
    multiple=True,
    type=str,
    help="specify custom columns names for each column in the CSV input file",
)
def csv_to_json(csv_file_name, out_file_name, has_headers, custom_headers):
    """Specify an input CSV file to convert to JSON.

    If desired, you can provide custom column names using the `--columns` option.

    Note that if you do not specify custom headers using --columns, then you **must**
    use the --has-headers flag.
    """
    convert_csv_to_json(
        csv_file_name=csv_file_name,
        out_file_name=out_file_name,
        has_headers=has_headers,
        custom_headers=custom_headers,
    )


converters_group.add_command(csv_to_json)
