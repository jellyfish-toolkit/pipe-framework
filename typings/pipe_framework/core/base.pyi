from typing import (
    Any,
    Callable,
    Generic,
    Iterable,
    Iterator,
    List,
    MutableSequence,
    NamedTuple,
    ParamSpec,
    Protocol,
    TypedDict,
    TypeVar,
    runtime_checkable,
)

PipeType_co = TypeVar("PipeType_co", covariant=True)
StepType = TypeVar("StepType")
StateType = TypeVar("StateType")
DataType = TypeVar("DataType", covariant=True)
Runner = Callable[[PipeType_co, Hooks], StateType | None]
HooksArgs = ParamSpec("HooksArgs")

class Hooks(NamedTuple):
    before: Callable
    after: Callable
    interrupt: Callable[..., bool]

class Step(Generic[StateType], Protocol):
    def __call__(self, state: StateType) -> StateType: ...

@runtime_checkable
class Pipe(Generic[StepType, StateType], Iterable, Protocol):
    def __init__(
        self,
        steps: MutableSequence[StepType],
        state: StateType,
        hooks: Hooks,
    ) -> None: ...
    def __call__(self) -> Any: ...
    def __iter__(self) -> Iterator[StepType]: ...
    def __len__(self) -> int: ...
    def add(self, step: StepType) -> "SimplePipe": ...
    def set_state(self, state: StateType) -> "SimplePipe": ...
    def get_state(self) -> StateType: ...
    def set_runner(self, runner: Runner) -> "SimplePipe": ...
    def get_runner(self) -> Runner: ...

class SimplePipe(Pipe[Step, TypedDict]):
    def __init__(
        self, steps: List[Step], state, hooks: Hooks, runner: Runner
    ) -> None: ...
