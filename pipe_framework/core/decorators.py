from functools import wraps
from typing import Callable


def step(fn: Callable) -> Callable:
    """Decorator to convert function to step.

    :param step_fn: function to convert :return: pipe step
    """

    @wraps(fn)
    def step(*args, **kwargs):
        return fn(*args, **kwargs)

    return step
