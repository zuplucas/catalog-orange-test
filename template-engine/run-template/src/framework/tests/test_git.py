import shutil
from pathlib import Path
from unittest import TestCase

from templateframework.utils.git import commit_all_files, init_git


class Test(TestCase):
    def test_commit_all_files(self):
        target_path = Path("/tmp/test_utils_git/")
        shutil.rmtree(target_path, ignore_errors=True)
        target_path.mkdir(parents=True)

        init_git(target_path)
        target_path.joinpath("text.txt").write_text("some data")

        commit_id = commit_all_files(target_path, "just a test")
        self.assertNotEqual("", commit_id)
        self.assertIsNotNone(commit_id)
        self.assertFalse('"' in commit_id)
        self.assertFalse("'" in commit_id)
        self.assertFalse('\n' in commit_id)
