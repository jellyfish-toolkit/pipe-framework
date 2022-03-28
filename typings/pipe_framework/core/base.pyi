from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableSequence,
    Protocol,
    Sequence,
    Sized,
    TypedDict,
    TypeVar,
)

PipeType_co = TypeVar("PipeType_co", covariant=True)
StepType = TypeVar("StepType")
StateType = TypeVar("StateType")
DataType = TypeVar("DataType", covariant=True)
Runner = Callable[[PipeType_co, Hooks], StateType | None]

class Hooks(Generic[StateType], Protocol):
    def before_pipe(self, state: StateType) -> StateType: ...
    def after_pipe(self, state: StateType) -> StateType: ...
    def interrupt(self, state: StateType) -> bool: ...

class Step(Generic[StateType], Protocol):
    def __call__(self, state: StateType) -> StateType: ...

# PipeType type variable will be deprecated as soon as python 3.11 is released
# (see https://peps.python.org/pep-0673/)
class Pipe(Generic[PipeType_co, StepType, StateType], Iterator, Protocol):
    def __init__(
        self,
        steps: MutableSequence[StepType],
        state: StateType,
        hooks: Hooks[StateType],
        runner: Runner,
    ) -> None: ...
    def __call__(self) -> Any: ...
    def __iter__(self) -> Iterator[StepType]: ...
    def __len__(self) -> int: ...
    def add(self, step: StepType) -> PipeType_co: ...
    def set_state(self, state: StateType) -> PipeType_co: ...
    def get_state(self) -> StateType: ...
    def set_runner(self, runner: Runner) -> PipeType_co: ...
    def get_runner(self) -> Runner: ...

class SimplePipe(Pipe["SimplePipe", Step, TypedDict]):
    def __init__(self, steps: List[Step], state, hooks, runner) -> None: ...
