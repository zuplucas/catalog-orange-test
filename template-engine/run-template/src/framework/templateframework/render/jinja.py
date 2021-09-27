import json
from pathlib import Path

import unidecode
from jinja2 import FileSystemLoader

from templateframework.metadata import Metadata
from templateframework.utils.jinja import generate_env


def group_id_folder(value):
    return str(value).replace(".", "/")


def to_unidecode(value):
    return unidecode.unidecode(value)


class JinjaRender:
    def __init__(
            self,
            template_data_path: Path,
            metadata: Metadata,
            callbacks=None
    ):

        if callbacks is None:
            self.callbacks = []
        else:
            self.callbacks = callbacks

        env, env_vars = generate_env(metadata)
        env.loader = FileSystemLoader(
            str(
                template_data_path
            )
        )

        self.env = env
        self.envs_vars = env_vars
        self.template_data_path = template_data_path
        self.target_dir = metadata.target_path
        config_file = template_data_path.joinpath(".template_framework_config")
        self.ignore_paths = []
        if config_file.exists():
            config = json.loads(config_file.read_text())
            self.ignore_paths = config.get("ignorePaths", [])

    def render_data(self, sub_dir_origin: Path, sub_dir_target: Path):
        if sub_dir_origin.name in [".folder_name_config", ".template_framework_config"]:
            return
        sub_dir_origin_str = str(sub_dir_origin).replace("\\", "/")
        ignore = False
        for path in self.ignore_paths:
            if Path(sub_dir_origin_str).match(path):
                ignore = True
        if ignore:
            data = self.template_data_path.joinpath(sub_dir_origin).read_text()
        else:
            data = self.env.get_template(sub_dir_origin_str).render(self.envs_vars)
        for callback in self.callbacks:
            data = callback.render(data, sub_dir_origin, sub_dir_target)
        target_full_path = Path(self.target_dir).joinpath(sub_dir_target)
        if not target_full_path.exists():
            target_full_path.touch(
                mode=self.template_data_path.joinpath(sub_dir_origin).stat().st_mode)
        target_full_path.write_text(data)

    def render_folder_name(self, folder: Path) -> str:
        folder_name_config = folder.joinpath(".folder_name_config")
        if folder_name_config.exists():
            config = folder_name_config.read_text()
            return self.env.from_string(config).render(self.envs_vars)
        else:
            return self.env.from_string(folder.name).render(self.envs_vars)
