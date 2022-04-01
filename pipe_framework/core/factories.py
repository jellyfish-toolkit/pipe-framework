from typing import Generic, Tuple, TypeVar

from pipe_framework.core.base import Hooks, SimplePipe, Step


def create_hooks(*, before=None, after=None, interrupt=None):
    bypass = lambda x: x

    return Hooks(
        before=before or bypass,
        after=after or bypass,
        interrupt=interrupt or (lambda s: False),
    )


T = TypeVar("T")


# class create_simple_pipe(Generic[T]):
#     def __new__(
#         cls, callables: Tuple[Step[T], ...], state: T, hooks: Hooks | None = None
#     ):
#         if hooks is None:
#             hooks = create_hooks()

#         _pipe = SimplePipe(callables, state, hooks)

#         return _pipe


def create_simple_pipe(
    callables: Tuple[Step[T], ...], state: T, hooks: Hooks | None = None
) -> SimplePipe[T]:
    if hooks is None:
        hooks = create_hooks()

    _pipe = SimplePipe(callables, state, hooks)

    return _pipe
