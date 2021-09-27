from pathlib import Path


def add_dependence(out_path, dependence):
    gradle_path = Path(out_path).joinpath("build.gradle.kts")
    gradle_data = gradle_path.read_text()
    if dependence not in gradle_data:
        gradle_data = gradle_data.replace(
            "dependencies {\n",
            "dependencies {\n    " + dependence + "\n")
        gradle_path.write_text(gradle_data)


def delete_dependence(out_path, dependence):
    gradle_path = Path(out_path).joinpath("build.gradle.kts")
    gradle_data = gradle_path.read_text()
    if dependence in gradle_data:
        gradle_data = gradle_data.replace("\n    " + dependence + "\n", "\n")
        gradle_path.write_text(gradle_data)
