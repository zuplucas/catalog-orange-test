import os

import questionary
from questionary import Choice

from templateframework.storage.history_folder import HistoryFolder, GLOBAL_INPUTS_KEY
from templateframework.storage.otd import Otd


class QuestionaryPrompt:
    def __init__(self, template_path):
        self.template_path = template_path

    def inputs(self, target):
        history_folder = HistoryFolder(target)
        result = dict()
        envs = os.environ.copy()
        saved_inputs = history_folder.load_inputs().get(GLOBAL_INPUTS_KEY)
        if saved_inputs is None:
            saved_inputs = dict()

        otd = Otd(template_path=self.template_path)
        for prompt_input in otd.inputs:
            env_name = "INPUTS_{}".format(str(prompt_input.name).upper())
            env_value = envs.get(env_name)
            if env_value is not None and env_name != "":
                result[prompt_input.name] = resolve_env(
                    prompt_input, env_value)
            else:
                result[prompt_input.name] = resolve_value(
                    prompt_input, saved_inputs)
        return result


def resolve_value(prompt_input, saved_inputs: dict):
    if prompt_input.type == "bool":
        return resolve_bool(prompt_input, saved_inputs)
    if prompt_input.type == "password":
        return resolve_password(prompt_input)
    if prompt_input.type == "multiselect":
        return resolve_multiselect(prompt_input, saved_inputs)
    if prompt_input.type == "text":
        return resolve_text(prompt_input, saved_inputs)
    if prompt_input.type == "int":
        return resolve_int(prompt_input, saved_inputs)
    raise RuntimeError(
        "resolver not found for input with type {}".format(
            prompt_input.type))


def resolve_int(prompt_input, saved_inputs):
    default = saved_inputs.get(prompt_input.name)
    if default is None or not prompt_input.cache:
        default = prompt_input.default
        if default is None:
            default = ""
    if not isinstance(default, str):
        default = str(default)
    return int(
        questionary.text(
            prompt_input.label,
            default=default).unsafe_ask())


def resolve_text(prompt_input, saved_inputs):
    if prompt_input.items is None:
        default = saved_inputs.get(prompt_input.name)
        if default is None or not prompt_input.cache:
            default = prompt_input.default
            if default is None:
                default = ""
        if not isinstance(default, str):
            default = str(default)
        return questionary.text(
            prompt_input.label,
            default=default).unsafe_ask()
    else:
        default = saved_inputs.get(prompt_input.name)
        if default is None or not prompt_input.cache:
            default = prompt_input.default
        if not isinstance(default, str):
            default = str(default)
        return questionary.select(
            prompt_input.label, prompt_input.items, default=default
        ).unsafe_ask()


def resolve_multiselect(prompt_input, saved_inputs):
    default = saved_inputs.get(prompt_input.name)
    if default is None or not prompt_input.cache:
        default = prompt_input.default
        if default is None:
            default = []
    default_map = dict()
    for value in default:
        default_map[value] = True

    choices = []
    for item in prompt_input.items:
        choice = Choice(
            title=item,
            checked=bool(default_map.get(item))
        )
        choices.append(choice)
    return questionary.checkbox(
        prompt_input.label,
        choices=choices).unsafe_ask()


def resolve_password(prompt_input):
    return questionary.password(prompt_input.label).unsafe_ask()


def resolve_bool(prompt_input, saved_inputs):
    default = saved_inputs.get(prompt_input.name)
    if default is None or not prompt_input.cache:
        default = prompt_input.default
        if default is None:
            default = True
    if not isinstance(default, bool):
        default = bool(default)
    return questionary.confirm(
        prompt_input.label,
        default=default,
        auto_enter=False).unsafe_ask()


def resolve_env(prompt_input, env_value):
    if prompt_input.type == "bool":
        return bool(env_value)
    if prompt_input.type == "password":
        return env_value
    if prompt_input.type == "multiselect":
        return env_value.split("|-|")
    if prompt_input.type == "text":
        return env_value
    if prompt_input.type == "int":
        return int(env_value)
    raise RuntimeError(
        "resolver not found for input with type {}".format(
            prompt_input.type))


def envs_for_inputs(inputs: dict):
    envs = os.environ.copy()
    for k, v in inputs.items():
        if type(v) == list:
            envs["INPUTS_{}".format(str(k)).upper()] = "|-|".join(v)
        else:
            envs["INPUTS_{}".format(str(k)).upper()] = str(v)
    return envs
