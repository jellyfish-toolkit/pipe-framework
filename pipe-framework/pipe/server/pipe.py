import typing as t

from pipe.core.base import BasePipe, Step
from pipe.core.exceptions import PipeException
from pipe.server.wrappers import PipeResponse, make_response


class HTTPPipe(BasePipe):
    """Pipe structure for the `server` package.

    Pipe structure. Contains two parts - pipe for request and pipe for response.
    Data goes in next way
    (in): request extractor -> request transformer -> request loader
    (out): response extractor -> response transformer -> response loader

    """

    pipe_schema: t.Dict[str, t.Dict[str, t.Iterable[Step]]] = {}

    def __init__(self, request, values, *args, **kwargs):
        self.__request = request
        self.__values = values

        super(HTTPPipe, self).__init__(dict(request=request, **values), *args, **kwargs)

    @property
    def request(self):
        """Getter for request object
        """
        return self.__request

    @property
    def values(self):
        """Getter for values
        """
        return self.__values

    def interrupt(self, store):
        # If some step returned response, we should catch it
        return issubclass(store.__class__, PipeResponse) or isinstance(
            store, PipeResponse
        )

    def run_pipe(self):
        """The main method.
        Takes data and pass through pipe. Handles request and response

        :raises: PipeException

        """
        pipe_to_run = self.pipe_schema.get(self.request.method, None)

        if pipe_to_run is None:
            return make_response('method isn\'t supported', status=400)

        self._run_pipe(pipe_to_run.get('in', ()))
        return self._run_pipe(pipe_to_run.get('out', ()))
