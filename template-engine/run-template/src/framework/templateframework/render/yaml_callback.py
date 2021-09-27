from pathlib import Path

import hiyapyco


class YamlCallback:
    def __init__(self, target_path):
        self.target_path = Path(target_path)

    def render(self, data, sub_dir_origin, sub_dir_target):
        sub_dir_origin = Path(sub_dir_origin)
        if sub_dir_origin.suffix not in [".yaml", ".yml"]:
            return data

        target_path = self.target_path.joinpath(sub_dir_target)
        if not target_path.exists():
            return data

        target_data = target_path.read_text()
        if len(data) == 0:
            return target_data

        if len(target_data) == 0:
            return data

        merged_yaml = hiyapyco.load(
            [target_data, data], method=hiyapyco.METHOD_MERGE)
        return str(hiyapyco.dump(merged_yaml))
