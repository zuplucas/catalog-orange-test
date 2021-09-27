from pathlib import Path

import yaml


def remove_key_from_file(key, target):
    target_path = Path(target)
    if target_path.exists():
        target_data = target_path.read_text()
        target_yaml = yaml.load(target_data, Loader=yaml.Loader)
        remove_key(key, target_yaml)
        target_path.write_text(yaml.dump(target_yaml))


def remove_key(key, data):
    keys = key.split(".")
    if len(keys) == 1:
        data.pop(keys[0])
    else:
        new_keys = '.'.join(keys[1:])
        new_data = data[keys[0]]
        if new_data is not None:
            remove_key(new_keys, new_data)
