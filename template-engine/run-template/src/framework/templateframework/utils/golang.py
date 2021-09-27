from pathlib import Path


def add_go_func(filepath, func, imports):
    file_path = Path(filepath)
    file_data = file_path.read_text()
    new_file_data = file_data + "\n" + func
    new_file_data = new_file_data.replace(
        "import (", "import (\n\t" + '"' + imports + '"')
    file_path.write_text(new_file_data)


def remove_go_func(filepath, func, imports):
    file_path = Path(filepath)
    file_data = file_path.read_text()
    new_file_data = file_data.replace(func, "")
    new_file_data = new_file_data.replace('\t"' + imports + '"\n', "")
    file_path.write_text(new_file_data)


def add_code_to_main_func(filepath, code, imports=None):
    file_path = Path(filepath)
    file_data = file_path.read_text()
    new_file_data = file_data.replace(
        "func main() {", "func main() {\n" + code)
    if imports is not None:
        new_file_data = new_file_data.replace(
            "import (", "import (\n\t" + '"' + imports + '"')
    file_path.write_text(new_file_data)


def remove_code_to_main_func(filepath, code, imports=None):
    file_path = Path(filepath)
    file_data = file_path.read_text()
    new_file_data = file_data.replace(code, "")
    if imports is not None:
        new_file_data = new_file_data.replace('\t"' + imports + '"\n', "")
    file_path.write_text(new_file_data)
