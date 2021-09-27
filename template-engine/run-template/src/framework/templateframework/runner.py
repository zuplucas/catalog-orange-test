import os
import shutil
import subprocess
import sys
from pathlib import Path

from templateframework.config import TEMPLATES_FOLDER_NAME, DEFAULT_TEMPLATE_FOLDER_NAME, TEMPLATE_LOCAL_FILENAME_ENV, \
    SAMPLE_FOLDER_NAME_ENV
from templateframework.prompt.questionary_prompt import QuestionaryPrompt, envs_for_inputs
from templateframework.storage.history_folder import HISTORY_FOLDER
from templateframework.storage.otd import Otd
from templateframework.template import Template


def run(custom_templates: dict):
    home = Path().cwd()
    argv = sys.argv
    if len(argv) >= 3 and argv[1] == "apply":
        template = argv[2]
        target = str(Path.cwd().absolute())
        if len(argv) == 4:
            target = str(Path(argv[3]).absolute())
        _apply_local_template(home, template, custom_templates, target)


def apply_template(
        template: str,
        target: Path,
        inputs: dict,
        sample_folder: str,
        home: Path = None,
        template_path=None,
        keep_history_folder=False,
):
    if home is None:
        home = Path().cwd()
    if template_path is None:
        template_path = _find_template_path(home, template)

    if target.joinpath(HISTORY_FOLDER).exists():
        keep_history_folder=True

    template_data_path = template_path.joinpath(DEFAULT_TEMPLATE_FOLDER_NAME)
    prompt = QuestionaryPrompt(template_path)
    local_filename = os.environ.get(TEMPLATE_LOCAL_FILENAME_ENV)
    main_script = home.joinpath("main.py")

    if not main_script.exists():
        os.environ = envs_for_inputs(inputs)
        Template().run(
            prompt=prompt,
            template_data_path=template_data_path,
            target=str(target.absolute()),
            local_filename=local_filename,
            sample_folder=sample_folder,
        )
    else:
        envs = envs_for_inputs(inputs)
        if sample_folder is not None:
            envs[SAMPLE_FOLDER_NAME_ENV] = sample_folder
        subprocess.check_call(
            [
                sys.executable,
                "main.py",
                "apply",
                template,
                str(target.absolute())
            ],
            env=envs,
            cwd=str(home),
        )

    # Todo remove Hot Fix
    if not keep_history_folder:
        shutil.rmtree(target.joinpath(HISTORY_FOLDER), ignore_errors=True)


def _apply_local_template(home, template, custom_templates, target):
    template_path = _find_template_path(home, template)

    template_data_path = template_path.joinpath(DEFAULT_TEMPLATE_FOLDER_NAME)
    prompt = QuestionaryPrompt(template_path)
    local_filename = os.environ.get(TEMPLATE_LOCAL_FILENAME_ENV)

    sample_folder = None
    sample_folder_env = os.environ.get(SAMPLE_FOLDER_NAME_ENV)
    if sample_folder_env is not None:
        sample_folder = sample_folder_env

    template_class = custom_templates.get(template)
    if template_class is None:
        Template().run(
            prompt=prompt,
            template_data_path=template_data_path,
            target=target,
            local_filename=local_filename,
            sample_folder=sample_folder,
        )
    else:
        template_class.run(
            prompt=prompt,
            template_data_path=template_data_path,
            target=target,
            local_filename=local_filename,
            sample_folder=sample_folder,
        )


def _find_template_path(home, template):
    for folder in home.joinpath(TEMPLATES_FOLDER_NAME).iterdir():
        if not folder.is_dir():
            continue
        try:
            otd = Otd(folder)
            if otd.name == template:
                return folder
        except RuntimeError:
            pass
    raise RuntimeError(f"template {template} not found")
