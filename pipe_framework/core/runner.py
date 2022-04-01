from typing import TypeVar

from core.base import Runner, SimplePipe

T = TypeVar("T")


class __run_simple_factory(Runner[T]):
    """Run the pipe.

    :param pipe: The pipe to run. :param hooks: The hooks to wrap the
    pipe with. :return: The result of the pipe.
    """

    def __call__(self, pipe: SimplePipe[T]) -> T:
        # get initial state for pipe
        pipe.set_state(pipe.hooks.before(pipe.get_state()))

        for step in pipe:
            result = step(pipe.get_state())
            pipe.set_state(result)

            if pipe.hooks.interrupt(pipe.get_state()):
                break

        return pipe.hooks.after(pipe.get_state())


run_simple = __run_simple_factory()
