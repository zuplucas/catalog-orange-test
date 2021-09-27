class PromptMock:
    def __init__(self, inputs_mock):
        self.inputs_mock = inputs_mock

    def inputs(self, target):
        return self.inputs_mock
