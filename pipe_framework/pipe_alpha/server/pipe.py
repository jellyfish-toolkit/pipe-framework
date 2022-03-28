import typing as t

from frozendict import frozendict
from pipe.core.base import BasePipe, Step
from pipe.server.wrappers import PipeRequest, PipeResponse, make_response


class HTTPPipe(BasePipe):
    """Pipe structure for the `server` package."""

    pipe_schema: t.Dict[str, t.Dict[str, t.Iterable[Step]]] = {}

    def __init__(self, request, initial, *args, **kwargs):
        self.__request = request

        super(HTTPPipe, self).__init__(
            dict(request=request, **initial), *args, **kwargs
        )

    @property
    def request(self) -> PipeRequest:
        """Getter for request object."""
        return self.__request

    def interrupt(self, store) -> bool:
        # If some step returned response, we should interrupt `pipe` execution
        return issubclass(store.__class__, PipeResponse) or isinstance(
            store, PipeResponse
        )

    def run_pipe(self) -> frozendict:
        """The main method. Takes data and pass through pipe. Handles request
        and response.

        :raises: PipeException
        """
        pipe_to_run = self.pipe_schema.get(self.request.method, None)

        if pipe_to_run is None:
            return make_response("method isn't supported", status=400)

        self._run_pipe(pipe_to_run.get("in", ()))
        return self._run_pipe(pipe_to_run.get("out", ()))
