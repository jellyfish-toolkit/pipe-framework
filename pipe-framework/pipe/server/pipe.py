import typing as t

from pipe.core.base import BasePipe, Step
from pipe.server.wrappers import PipeResponse


class HTTPPipe(BasePipe):
    """Main structure in the framework. Represent pipe through which all data pass.

    Pipe structure. Contains two parts - pipe for request
    and pipe for response.
    Data goes in next way
    request -> request extractor -> request transformer -> request loader ->
    response extractor -> response transformer -> response loader

    """

    pipe_schema: t.Dict[str, t.Dict[str, t.Iterable[Step]]] = {}

    def __init__(self, request, *args, **kwargs):
        self.__request = request

        super(HTTPPipe, self).__init__(*args, **kwargs)

    @property
    def request(self):
        """Getter for request object

        """
        return self.__request

    def should_return(self, result):
        # If some loader returned response, we should catch it
        if issubclass(result.__class__, PipeResponse) or isinstance(result, PipeResponse):
            return result

    def run_pipe(self):
        """The main method.
        Takes data and pass through pipe. Handles request and response

        :raises: PipeException

        """

        self.store = self.store.copy(request=self.request)

        pipe_to_run = self.pipe_schema.get(self.request.method, {'in': (), 'out': ()})

        self._run_pipe(pipe_to_run.get('in', ()))
        result = self._run_pipe(pipe_to_run.get('out', ()))

        return result
