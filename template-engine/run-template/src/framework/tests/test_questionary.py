import os
from pathlib import Path
from unittest import TestCase

from templateframework.prompt.questionary_prompt import QuestionaryPrompt


class TestQuestionaryPrompt(TestCase):
    def test_inputs(self):
        target_path = Path("./test_data")

        os.environ["INPUTS_INPUT_TEXT"] = "any_text"
        os.environ["INPUTS_INPUT_PASSWORD"] = "any_pass"
        os.environ["INPUTS_INPUT_BOOL"] = "true"
        os.environ["INPUTS_INPUT_INT"] = "42"
        os.environ["INPUTS_ANY_TEXT_WITH_ITEMS"] = "python"
        os.environ["INPUTS_INPUT_DAYS"] = "Monday|-|Tuesday"

        inputs = QuestionaryPrompt(target_path).inputs(target_path)
        self.assertEqual(inputs["input_text"], "any_text")
        self.assertEqual(inputs["input_password"], "any_pass")
        self.assertEqual(inputs["input_bool"], True)
        self.assertEqual(inputs["input_int"], 42)
        self.assertEqual(inputs["any_text_with_items"], "python")
        self.assertEqual(inputs["input_days"], ["Monday", "Tuesday"])
        self.assertEqual(inputs.__len__(), 6)
