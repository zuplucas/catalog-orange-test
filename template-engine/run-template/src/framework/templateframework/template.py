from pathlib import Path

from templateframework.config import DEFAULT_TEMPLATE_FOLDER_NAME, DEFAULT_SAMPLE_FOLDER_NAME
from templateframework.metadata import Metadata
from templateframework.prompt.questionary_prompt import QuestionaryPrompt
from templateframework.render.diff_callback import DiffCallback
from templateframework.render.jinja import group_id_folder, JinjaRender, to_unidecode
from templateframework.render.json_callback import JsonCallback
from templateframework.render.yaml_callback import YamlCallback
from templateframework.storage.history_folder import HistoryFolder
from templateframework.utils.file import render_dir


class Template:
    def run(
            self,
            prompt=None,
            template_data_path=None,
            target=None,
            local_filename=None,
            sample_folder=None,
    ):
        if local_filename is None:
            local_filename = "last.json"
        if target is None or target == "":
            target = "."
        if template_data_path is None:
            template_data_path = Path().cwd().joinpath(DEFAULT_TEMPLATE_FOLDER_NAME)
        if prompt is None:
            prompt = QuestionaryPrompt(template_data_path.parent)

        metadata = Metadata(
            target_path=Path(target),
            inputs=prompt.inputs(target),
            history_folder=HistoryFolder(target),
            history_local_filename=local_filename,
            sample=sample_folder is not None,
            sample_folder=sample_folder,
            filters=dict(),
        )
        self.apply(metadata, template_data_path, sample_folder)

    def pre_hook(self, metadata: Metadata) -> Metadata:
        return metadata

    def post_hook(self, metadata: Metadata):
        pass

    def apply(self, metadata: Metadata, template_data_path: Path, sample_folder: str):
        metadata.filters["group_id_folder"] = group_id_folder
        metadata.filters["to_unidecode"] = to_unidecode

        metadata = self.pre_hook(metadata)

        apply_target(metadata, template_data_path)
        if metadata.sample:
            template_sample_data_path = template_data_path.parent.joinpath(sample_folder)
            if template_sample_data_path.exists():
                apply_target(metadata, template_sample_data_path)

        self.post_hook(metadata)


def apply_target(metadata, template_data_path):
    diff_callback = DiffCallback(metadata.target_path)
    json_callback = JsonCallback(metadata.target_path)
    yaml_callback = YamlCallback(metadata.target_path)
    callbacks = [diff_callback, json_callback, yaml_callback]
    jinja_render = JinjaRender(
        template_data_path,
        metadata,
        callbacks=callbacks,
    )
    render_dir(jinja_render, template_data_path, metadata.target_path)
    metadata.history_folder.save_inputs(metadata.inputs)
