from __future__ import annotations

from typing import (
    Callable,
    Generic,
    Iterable,
    Iterator,
    NamedTuple,
    Protocol,
    Tuple,
    TypeVar,
)

from core.runner import run_simple

StateType = TypeVar("StateType")
DataType = TypeVar("DataType", covariant=True)
# Runner = Callable[["Pipe"[StateType]], StateType]


class Runner(Generic[StateType], Protocol):
    def __call__(self, pipe: "Pipe"[StateType]) -> StateType:
        ...


class Hooks(NamedTuple):
    before: Callable
    after: Callable
    interrupt: Callable[..., bool]


class Step(Generic[StateType], Protocol):
    def __call__(self, state: StateType) -> StateType:
        ...


class Pipe(Generic[StateType], Iterable, Protocol):
    hooks: Hooks
    state: StateType
    steps: Tuple[Step[StateType], ...]
    run: Runner[StateType]

    def __init__(
        self,
        steps: Tuple[Step[StateType], ...],
        state: StateType,
        hooks: Hooks,
        runner: Runner[StateType],
    ) -> None:
        ...

    def __call__(self) -> StateType:
        ...

    def __iter__(self) -> Iterator[Step[StateType]]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, step: Step) -> "Pipe":
        ...

    def get_state(self) -> StateType:
        ...

    def set_state(self, state: StateType) -> "Pipe":
        ...

    def set_runner(self, runner: Runner[StateType]) -> "Pipe":
        ...

    def get_runner(self) -> Runner[StateType]:
        ...

    def handle_interrupt(self) -> bool:
        ...


class SimplePipe(Generic[StateType], Pipe[StateType]):
    def __init__(
        self,
        steps: Tuple[Step[StateType], ...],
        state: StateType,
        hooks,
        runner: Runner[StateType] = run_simple,
    ):
        self.steps = steps
        self.set_runner(runner)
        self.set_hooks(hooks)
        self.state = state

    def set_steps(self, steps):
        map(self.add, steps)

        return self

    def get_state(self):
        return self.state

    def set_state(self, state: StateType):
        self.state = state

    def add(self, step):
        self.steps = self.steps + (step,)

        return self

    def set_runner(self, runner: Runner[StateType]):
        self.run = runner

    def set_hooks(self, hooks):
        self.hooks = hooks

        return self

    def get_runner(self):
        return self.run

    def handle_interrupt(self):
        # TODO: figure out how to handle this
        return self.hooks.interrupt()

    def __iter__(self):
        return iter(self.steps)

    def __len__(self):
        return len(self.steps)

    def __call__(self):
        return self.run(self)
