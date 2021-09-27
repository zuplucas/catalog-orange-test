import json
from pathlib import Path

from jsonmerge import merge


class JsonCallback:
    def __init__(self, target_path):
        self.target_path = Path(target_path)

    def render(self, data, sub_dir_origin, sub_dir_target):
        sub_dir_origin = Path(sub_dir_origin)
        if sub_dir_origin.suffix != ".json":
            return data

        target_path = self.target_path.joinpath(sub_dir_target)
        if not target_path.exists():
            return data

        merged = merge(json.loads(data), json.loads(target_path.read_text()))
        return json.dumps(merged, indent=4)
