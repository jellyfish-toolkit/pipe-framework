from typing import TYPE_CHECKING


def run_simple(pipe: SimplePipe, hooks: Hooks):
    """
    Run the pipe

    :param pipe: The pipe to run.
    :param hooks: The hooks to wrap the pipe with.
    :return: The result of the pipe.
    """
    # first we set initial state to the pipe
    pipe.set_state(hooks.before_pipe(pipe.get_state()))
