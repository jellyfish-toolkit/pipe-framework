from typing import TYPE_CHECKING, TypedDict

if TYPE_CHECKING:
    from pipe_framework.core.base import Hooks, SimplePipe


def run_simple(pipe: SimplePipe, hooks: Hooks[TypedDict]) -> TypedDict:
    """
    Run the pipe

    :param pipe: The pipe to run.
    :param hooks: The hooks to wrap the pipe with.
    :return: The result of the pipe.
    """

    # first we set initial state to the pipe
    pipe.set_state(hooks.before_pipe(pipe.get_state()))

    for step in pipe:
        result = step(pipe.get_state())
        pipe.set_state(result)

        if hooks.interrupt(pipe.get_state()):
            break

    return hooks.after_pipe(pipe.get_state())
