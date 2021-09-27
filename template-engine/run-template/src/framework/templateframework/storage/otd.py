from pathlib import Path

import yaml


class Otd:
    def __init__(self, template_path: Path):
        otc_filename = "orange-template*.yml"
        otc_path = None
        for file in template_path.iterdir():
            if file.match(otc_filename):
                otc_path = file
        if otc_path is None:
            raise RuntimeError(
                "{} not found at {}".format(
                    otc_filename,
                    str(template_path)))

        otc_yaml = yaml.load(otc_path.read_text(), Loader=yaml.Loader)
        self.type = otc_yaml.get("type")
        self.tags = otc_yaml.get("tags")
        self.name = otc_yaml.get("name")
        self.ask_sample = otc_yaml.get("haveSample", False)
        self.description = otc_yaml.get("description")
        self.inputs = []
        inputs = otc_yaml.get("inputs")
        if inputs is not None:
            for input_yml in inputs:
                prompt_input = PromptInput(input_yml)
                self.inputs.append(prompt_input)


class PromptInput:
    def __init__(self, input_dict):
        self.label = input_dict.get("label")
        self.type = input_dict.get("type")
        self.default = input_dict.get("default")
        self.name = input_dict.get("name")
        self.items = input_dict.get("items")
        self.cache = input_dict.get("cache")
        if self.cache is None:
            self.cache = True
        self.check()

    def check(self):
        if self.label == "" or self.label is None:
            raise RuntimeError("input label is empty.")
        if self.name == "" or self.name is None:
            raise RuntimeError("input name is empty.")
        if self.type not in ["text", "password", "bool", "multiselect", "int"]:
            raise RuntimeError("{} is a invalid input type.".format(self.type))
