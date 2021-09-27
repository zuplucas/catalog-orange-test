import json
from pathlib import Path

HISTORY_FOLDER = ".template"
HISTORY_INPUT_FILE = "inputs.json"
GLOBAL_INPUTS_KEY = "global"
LAST_INPUTS_KEY = "last"


class HistoryFolder:
    def __init__(self, target_path):
        self.folder_path = Path(target_path).joinpath(HISTORY_FOLDER)
        self.inputs_file = self.folder_path.joinpath(HISTORY_INPUT_FILE)

        if not self.folder_path.exists():
            self.folder_path.mkdir(parents=True)
            self.inputs_file.write_text("{}")

    def save_inputs(self, inputs: dict):
        if inputs is None:
            return
        self.folder_path.joinpath(HISTORY_INPUT_FILE)
        saved_inputs = self.load_inputs()
        global_inputs = saved_inputs.get(GLOBAL_INPUTS_KEY)
        if global_inputs is not None:
            for key in inputs.keys():
                global_inputs[key] = inputs[key]
        else:
            saved_inputs[GLOBAL_INPUTS_KEY] = inputs
        saved_inputs[LAST_INPUTS_KEY] = inputs
        self.inputs_file.write_text(json.dumps(saved_inputs, indent=4))

    def load_inputs(self):
        return json.loads(self.inputs_file.read_text())

    def save_data(self, filename, key, data):
        file_path = self.get_file_path(filename)
        saved_data = json.loads(file_path.read_text())
        saved_data[key] = data
        file_path.write_text(json.dumps(saved_data, indent=4))

    def get_data(self, filename, key):
        file_path = self.get_file_path(filename)
        saved_data = json.loads(file_path.read_text())
        return saved_data.get(key)

    def get_file_path(self, filename):
        file_path = self.folder_path.joinpath(filename)
        if not file_path.exists():
            file_path.write_text("{}")
        return file_path
