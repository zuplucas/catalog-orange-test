from pathlib import Path


def add_dependence(out_path, name, version):
    gomod_path = Path(out_path).joinpath("go.mod")
    gomod_data = gomod_path.read_text()
    dependence = name + " " + version
    if dependence not in gomod_data:
        if "require (" not in gomod_data:
            split_data = gomod_data.split("require ")
            before_require = split_data[0]
            after_require_lines = split_data[1].splitlines(keepends=True)
            after_require_lines[0] = after_require_lines[0] + ")"
            gomod_data = before_require + \
                "require (\n\t" + "".join(after_require_lines)
        gomod_data = gomod_data.replace(
            "require (\n", "require (\n\t" + dependence + "\n")
        gomod_path.write_text(gomod_data)


def remove_dependence(out_path, name, version):
    gomod_path = Path(out_path).joinpath("go.mod")
    gomod_data = gomod_path.read_text()
    dependence = name + " " + version
    gomod_data = gomod_data.replace("\t" + dependence + "\n", "")
    gomod_path.write_text(gomod_data)
