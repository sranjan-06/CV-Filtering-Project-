class BaseAgent:
    def __init__(self, name):
        self.name = name

    def run(self, payload):
        raise NotImplementedError("Each agent must implement run().")