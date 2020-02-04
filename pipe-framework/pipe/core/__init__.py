"""Main module of the framework

"""
import typing as t
from dataclasses import dataclass, field

from werkzeug.exceptions import HTTPException
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

import pipe.core.base as base
import pipe.core.data as data
import pipe.core.interface as interface
import pipe.core.utils as utils

__all__ = ['app']


class AppException(Exception):
    pass


@dataclass
class App():
    """Main WSGI app wrapper which run pipes according to request

    """

    __paths: t.Dict[str, t.List[base.Pipe]] = None
    __map: Map = Map()

    def path(self, route: str):
        """Decorator for adding pipe as a handler for a route

        :param route: Werkzeug formatted route
        :type route: string
        """
        def decorator(pipe):

            if self.__paths is None:
                pipe_list = utils.PipeList()
                self.__paths = {route: pipe_list}
            else:
                pipe_list = self.__paths.get(route)

            pipe_list.add(pipe)

        return decorator

    def wsgi_app(self, environ, start_response):
        """Main WSGI app, see werkzeug documentation for more

        """
        request = Request(environ)
        adapter = self.__map.bind_to_environ(environ)

        try:
            endpoint, values = adapter.match()
        except HTTPException as e:
            return e(environ, start_response)

        for pipe in endpoint.get_pipes():
            result = pipe(request).run_pipe()

        if isinstance(result, Response):
            return result(environ, start_response)

        response = Response(status=204)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)

    def run(self, host: str = '127.0.0.1', port: int = 8000, *args, **kwargs):
        """Method for running application, actually pretty similar to the Flask run method

        :param host: which host use for serving, defaults to '127.0.0.1'
        :type host: str, optional
        :param port: which port to listen, defaults to 8000
        :type port: int, optional
        """

        for path, pipes in self.__paths.items():
            self.__map.add(Rule(path, endpoint=pipes))

        run_simple(host, port, self, *args, **kwargs)


app = App()
