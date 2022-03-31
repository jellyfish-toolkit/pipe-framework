from typing import Callable, Protocol, TypedDict

from pipe_framework.core.base import Hooks, SimplePipe


def pipe(*callables: Callable, **options) -> Callable:
    """
    Pipe a series of callables together.

    :param callables: A series of callables to pipe together.
    :param options: A dictionary of options to pass to the callables.
    :return: A callable that will call the callables in order.
    """
    hooks: Hooks[TypedDict] = options.get("hooks", {"before": [], "after": []})

    _pipe = SimplePipe(
        callables,
    )

    return _pipe
