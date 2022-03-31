from collections import namedtuple
from typing import Any, Callable, TypedDict

from pipe_framework.core.base import Hooks, SimplePipe


def hooks(
    *, before: Callable, after: Callable, interrupt: Callable[..., bool]
) -> Hooks:
    bypass = lambda x: x

    return Hooks(
        before=before or bypass,
        after=after or bypass,
        interrupt=interrupt or (lambda: False),
    )


def pipe(*callables: Callable, hooks: Hooks) -> Callable:
    """
    Pipe a series of callables together.

    :param callables: A series of callables to pipe together.
    :param options: A dictionary of options to pass to the callables.
    :return: A callable that will call the callables in order.
    """
    if hooks is None:
        hooks = hooks()

    _pipe = SimplePipe(callables, hooks)

    return _pipe
