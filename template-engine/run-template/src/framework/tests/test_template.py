import shutil
from pathlib import Path
from unittest import TestCase

from templateframework.metadata import Metadata
from templateframework.prompt.prompt_mock import PromptMock
from templateframework.template import Template


class MyTemplate(Template):

    def pre_hook(self, metadata: Metadata) -> Metadata:
        print("logic before apply")
        metadata.inputs["msg"] = "other msg"
        return metadata

    def post_hook(self, metadata: Metadata):
        print("logic after apply")


class TestTemplates(TestCase):
    def test_simple_template(self):
        inputs = {
            "msg": "any text"
        }
        template_data_path = Path("test_data/simple_template")
        target_path = Path("/tmp/test_simple_template")
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir()
        my_template = MyTemplate()
        my_template.run(
            target=target_path,
            template_data_path=template_data_path,
            prompt=PromptMock(inputs),
        )

        self.assertIn(
            inputs["msg"],
            target_path.joinpath("README.md").read_text())
        self.assertIn(inputs["msg"], target_path.joinpath(
            "some_dir/test.txt").read_text())
        self.assertIn(
            inputs["msg"].replace(
                " ",
                "_"),
            target_path.joinpath("some_dir/test.txt").read_text())

    def test_dynamic_folder_name_apply(self):
        inputs = {
            "msg": "any text",
            "folder_name": "dynamic_folder_name",
        }
        template_data_path = Path("test_data/dynamic_folder_name")
        target_path = Path("/tmp/test_dynamic_folder_name_apply")
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir()
        my_template = MyTemplate()

        my_template.run(
            target=target_path,
            template_data_path=template_data_path,
            prompt=PromptMock(inputs),
        )
        assert inputs["msg"] in target_path.joinpath("README.md").read_text()
        assert inputs["msg"] in target_path.joinpath(
            "dynamic_folder_name/test.txt").read_text()

    def test_sample_data(self):
        inputs = {
            "msg": "any text",
            "folder_name": "dynamic_folder_name",
        }
        template_data_path = Path("test_data/simple_template-data")
        target_path = Path("/tmp/test_sample-data")
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir()
        my_template = MyTemplate()

        my_template.run(
            target=target_path,
            template_data_path=template_data_path,
            sample_folder="simple_sample-data",
            prompt=PromptMock(inputs),
        )
        self.assertIn(
            inputs["msg"],
            target_path.joinpath("README.md").read_text(),
        )
        self.assertIn(
            inputs["msg"],
            target_path.joinpath("some_dir/test.txt").read_text(),
        )

    def test_ignore_paths(self):
        inputs = {
            "example": "any text",
        }
        template_data_path = Path("test_data/test_ignore_paths")
        target_path = Path("/tmp/test_ignore_paths")
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir()
        my_template = MyTemplate()

        my_template.run(
            target=target_path,
            template_data_path=template_data_path,
            prompt=PromptMock(inputs),
        )
        self.assertIn(
            "{{ some_var }}",
            target_path.joinpath("terraform/file.txt").read_text(),
        )
        self.assertIn(
            "{{ some_var }}",
            target_path.joinpath("some_folder/sub_dir/file.txt").read_text(),
        )
        self.assertIn(
            inputs["example"],
            target_path.joinpath("some_folder/file2.txt").read_text(),
        )
        self.assertIn(
            inputs["example"],
            target_path.joinpath("file2.txt").read_text(),
        )
        self.assertFalse(target_path.joinpath(".template_framework_config").exists())

    def test_inputs_with_name_sample(self):
        inputs = {
            "sample": True,
            "example": "some-text",
        }
        template_data_path = Path("test_data/input_with_name_sample")
        target_path = Path("/tmp/test_inputs_with_name_sample")
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir()
        my_template = MyTemplate()

        my_template.run(
            target=target_path,
            template_data_path=template_data_path,
            prompt=PromptMock(inputs),
            sample_folder=None,
        )
        self.assertIn(
            "hello True.",
            target_path.joinpath("README.md").read_text(),
        )
        self.assertIn(
            "this is a example: some-text",
            target_path.joinpath("README.md").read_text(),
        )
        self.assertNotIn(
            "not print this",
            target_path.joinpath("README.md").read_text(),
        )