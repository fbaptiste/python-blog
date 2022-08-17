import csv
from itertools import islice

from tabulate import tabulate

from viewers.enums import TableFormat


def preview_csv(
    file_name: str,
    first_n: int = None,
    has_header_row: bool = False,
    table_format: TableFormat = TableFormat.fancy_outline,
) -> str:
    with open(file_name) as f:
        data = csv.reader(f)

        if has_header_row:
            headers = next(data)
        else:
            headers = None

        if first_n:
            rows = list(islice(data, first_n))
        else:
            rows = list(data)

    if headers:
        return tabulate(rows, headers=headers, tablefmt=table_format.value)
    else:
        return tabulate(rows)
