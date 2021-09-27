import json
import shutil
from pathlib import Path
from unittest import TestCase

from templateframework.render.json_callback import JsonCallback


class TestJsonCallback(TestCase):
    def test_render(self):
        target_path = Path("/tmp/TestJsonCallback/")
        shutil.rmtree(target_path, ignore_errors=True)
        target_path.mkdir(parents=True)

        target_data = """
        {
            "name": "any_text",
            "type": "any_type"
        }
        """
        target_file = target_path.joinpath("text.json")
        target_file.write_text(target_data)

        template_data = """
        {
            "description": "any_description",
            "int": "any_int"
        }
        """
        result = JsonCallback(target_path).render(
            template_data, target_file.name, target_file.name)

        want = """
        {
            "description": "any_description",
            "int": "any_int",
            "name": "any_text",
            "type": "any_type"
        }
        """
        want = json.dumps(json.loads(want), indent=4)
        self.assertEqual(want, result)
