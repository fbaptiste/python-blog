import json


def preview_json(file_name: str, first_n: int = None, indent: int = 2) -> str:
    with open(file_name) as f:
        data = json.load(f)

    formatted_data = json.dumps(data, indent=indent)

    if indent == 0:
        result = formatted_data.replace("\n", "")
    else:
        formatted_data = formatted_data.split("\n")
        if first_n:
            formatted_data = formatted_data[:first_n]
        result = "\n".join(formatted_data)
    return result
