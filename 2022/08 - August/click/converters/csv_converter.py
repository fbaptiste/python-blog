import csv
import json


def _validate_header_count(csv_file_name: str, expected_column_count: int):
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        row = next(reader)
        if len(row) != expected_column_count:
            raise ValueError("Header count and actual CSV file column mismatch.")


def convert_csv_to_json(
    csv_file_name: str,
    out_file_name: str,
    has_headers: bool = False,
    custom_headers: list[str] = None,
):
    # If has_headers is False, then custom_headers *must* be provided
    if not has_headers and not custom_headers:
        raise ValueError("Headers must be provided if CSV does not contain them.")

    # Validate custom_headers count (if specified)
    if custom_headers:
        _validate_header_count(csv_file_name, len(custom_headers))

    # Instead of reading the entire CSV file into memory, we'll read
    # it in row by row, and output the JSON as the same time - more memory efficient
    with open(csv_file_name) as in_file:
        with open(out_file_name, "w") as out_file:
            csv_data = csv.reader(in_file)

            file_headers = next(csv_data) if has_headers else None
            csv_headers = custom_headers or file_headers

            out_file.write("[")
            first_element = True
            for row in csv_data:
                if first_element:
                    first_element = False
                else:
                    out_file.write(",")
                output_dict = dict(zip(csv_headers, row))
                out_file.write(json.dumps(output_dict, indent=0))
            out_file.write("]")
