import shutil
from pathlib import Path
from unittest import TestCase

from templateframework.render.diff_callback import DiffCallback


# Todo test not render json,yaml and file no exist
class TestDiffCallback(TestCase):
    def test_render(self):
        target_path = Path("/tmp/TestDiffCallback/")
        shutil.rmtree(target_path, ignore_errors=True)
        target_path.mkdir(parents=True)

        target_data = "require (\n"
        target_data += "  one\n"
        target_data += "  two\n"
        target_data += "  tree\n"
        target_data += ")"
        target_file = target_path.joinpath("text.txt")
        target_file.write_text(target_data)

        template_data = "require (\n"
        template_data += "  four\n"
        template_data += ")"
        result = DiffCallback(target_path).render(
            template_data, Path("."), target_file.name)

        want = "require (\n"
        want += "  four\n"
        want += "  one\n"
        want += "  two\n"
        want += "  tree\n"
        want += ")"

        self.assertEqual(want, result)

    def test_render_data(self):
        template_data_path = Path(
            "./test_data/gradle_dependence/new/build.gradle.kts")
        base_path = Path("./test_data/gradle_dependence/base/build.gradle.kts")
        tmp_file = Path("/tmp/test_render_data_diff/build.gradle.kts")
        if tmp_file.parent.exists():
            shutil.rmtree(tmp_file.parent)
        tmp_file.parent.mkdir()
        tmp_file.touch()
        tmp_file.write_text(base_path.read_text())

        diff_callback = DiffCallback(tmp_file.parent)
        result = diff_callback.render(
            template_data_path.read_text(),
            template_data_path.name,
            tmp_file.name
        )
        want_path = Path("./test_data/gradle_dependence/want/build.gradle.kts")
        self.assertEqual(want_path.read_text(), result)

    def test_render_with_append_to_end(self):
        target_path = Path("/tmp/TestDiffCallback/")
        shutil.rmtree(target_path, ignore_errors=True)
        target_path.mkdir(parents=True)

        target_data = "require (\n"
        target_data += "  one\n"
        target_data += "  two\n"
        target_data += "  tree\n"
        target_data += ")\n"
        target_data += "func a {\n"
        target_data += "  some other data where\n"
        target_data += "}\n"
        target_file = target_path.joinpath("text-append.txt")
        target_file.write_text(target_data)

        template_data = "require (\n"
        template_data += "  four\n"
        template_data += ")\n"
        template_data += "#scaffold: append-to-end-of-file\n"
        template_data += "func b {\n"
        template_data += "  any data where\n"
        template_data += "}\n"
        result = DiffCallback(target_path).render(
            template_data, Path("."), target_file.name)

        want = "require (\n"
        want += "  four\n"
        want += "  one\n"
        want += "  two\n"
        want += "  tree\n"
        want += ")\n"
        want += "func a {\n"
        want += "  some other data where\n"
        want += "}\n"
        want += "\nfunc b {\n"
        want += "  any data where\n"
        want += "}\n"

        self.assertEqual(want, result)
