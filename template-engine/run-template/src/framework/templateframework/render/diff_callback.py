import difflib
from pathlib import Path


class DiffCallback:
    def __init__(self, target_path):
        self.line_not_present_in_either_input_sequence = "? "
        self.target_path = Path(target_path)

    def render(self, data, sub_dir_origin, sub_dir_target):
        target_path = self.target_path.joinpath(sub_dir_target)
        if not target_path.exists():
            data = str(data).replace("#scaffold: append-to-end-of-file\n", "")
            return data

        sub_dir_origin = Path(sub_dir_origin)
        if sub_dir_origin.suffix in (".yaml", ".yml", ".json"):
            return data

        target_data = target_path.read_text()
        data_lines = data.splitlines(keepends=True)
        for i in range(0, len(data_lines)):
            if data_lines[i] == "#scaffold: append-to-end-of-file\n":
                target_data += "\n" + "".join(data_lines[i + 1:])
                data_lines = data_lines[0:i]
                break

        target_lines = target_data.splitlines(keepends=True)

        # não mudar a ordem .compare(
        #    data_lines,
        #    target_lines,
        # )
        # diferente de compare(
        #    target_lines,
        #    data_lines,
        # )
        diff = difflib.Differ().compare(
            data_lines,
            target_lines,
        )
        return self.concat_diff(diff)

    # only ignore lines not present in either input sequence
    def concat_diff(self, diff):
        result = ""
        for line in diff:
            if line[0:2] != self.line_not_present_in_either_input_sequence:
                result = result + line[2:]
        return result
