from __future__ import annotations

from pipe_framework.core.runner import run_simple


class SimplePipe:
    def __init__(
        self,
        steps,
        state,
        hooks,
        runner=run_simple,
    ):
        self.steps = steps
        self.set_runner(runner)
        self.set_hooks(hooks)
        self.state = state

    def set_steps(self, steps):
        for step in steps:
            self.add(step)

        return self

    def add(self, step):
        self.steps.append(step)

        return self

    def get_steps(self):
        return self.steps

    def set_runner(self, runner):
        self.run = runner

    def set_hooks(self, hooks):
        self.hooks = hooks

        return self

    def get_runner(self):
        return self.run

    def __iter__(self):
        return self.steps

    def __len__(self):
        return len(self.steps)

    def __call__(self):
        self.run(self, self.hooks)
