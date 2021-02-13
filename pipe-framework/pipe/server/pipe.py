import typing as t

from frozendict import frozendict

from pipe.core.base import BasePipe, Step
from pipe.server.wrappers import PipeResponse, make_response, PipeRequest


class HTTPPipe(BasePipe):
    """Pipe structure for the `server` package.

    Pipe structure. Contains two parts - pipe for request and pipe for response.
    Data goes in next way
    (in): request extractor -> request transformer -> request loader
    (out): response extractor -> response transformer -> response loader

    Example:

    ```python
    @app.route('/todo/')
    class TodoResource(HTTPPipe):
    pipe_schema = {
        'GET': {
            'out': (
                EDatabase(table_name='todo-items'), TJsonResponseReady(data_field='todo-items_list'), LJsonResponse()
            )
        },
        'POST': {
            'in': (EJsonBody(), LDatabase(data_field='json', table_name='todo-items')),
            'out': (
                TLambda(lambda_=lambda store: store.copy(id=store.get('todo-items_insert'))),
                EDatabase(table_name='todo-items'), TJsonResponseReady(data_field='todo-items_item'), LJsonResponse()
            )
        }
    }
    ```


    """

    pipe_schema: t.Dict[str, t.Dict[str, t.Iterable[Step]]] = {}

    def __init__(self, request, initial, *args, **kwargs):
        self.__request = request

        super(HTTPPipe, self).__init__(dict(request=request, **initial), *args, **kwargs)

    @property
    def request(self) -> PipeRequest:
        """Getter for request object
        """
        return self.__request

    def interrupt(self, store) -> bool:
        # If some step returned response, we should interrupt `pipe` execution
        return issubclass(store.__class__, PipeResponse) or isinstance(store, PipeResponse)

    def run_pipe(self) -> frozendict:
        """The main method.
        Takes data and pass through pipe. Handles request and response

        :raises: PipeException
        """
        pipe_to_run = self.pipe_schema.get(self.request.method, None)

        if pipe_to_run is None:
            return make_response('method isn\'t supported', status=400)

        self._run_pipe(pipe_to_run.get('in', ()))
        return self._run_pipe(pipe_to_run.get('out', ()))
