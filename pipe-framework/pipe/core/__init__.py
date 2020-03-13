"""Main module of the framework

"""
import typing as t
from dataclasses import dataclass, field

from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

import pipe.core.base as base
import pipe.core.data as data
import pipe.core.utils as utils

__all__ = ['app']


class AppException(Exception):
    pass


@dataclass
class App:
    """Main WSGI app wrapper which run pipes according to request

    """

    __paths: t.Dict[str, t.List[base.Pipe]] = None
    __map: Map = Map()
    __static_serving: bool = False
    __static_folder: t.Optional[str] = None
    __static_url: t.Optional[str] = None

    def path(self, route: str):
        """Decorator for adding pipe as a handler for a route

        :param route: Werkzeug formatted route
        :type route: string
        """
        def decorator(pipe):

            # TODO: a bit ugly, refactoring required
            if self.__paths is None:
                pipe_list = utils.PipeList()
                self.__paths = {route: pipe_list}
            elif not self.__paths.get(route, False):
                pipe_list = utils.PipeList()
                self.__paths.update({route: pipe_list})
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
        if self.__static_serving:
            app_with_static = SharedDataMiddleware(self.wsgi_app, {self.__static_url: self.__static_folder})
            return app_with_static(environ, start_response)
        else:
            return self.wsgi_app(environ, start_response)

    def run(
        self,
        host: str = '127.0.0.1',
        port: int = 8000,
        static_folder: t.Optional[str] = None,
        static_url: str = '/static',
        *args,
        **kwargs
    ):
        """Method for running application, actually pretty similar to the Flask run method

        :param host: which host use for serving, defaults to '127.0.0.1'
        :type host: str, optional
        :param port: which port to listen, defaults to 8000
        :type port: int, optional
        """

        if static_folder is not None:
            self.__static_serving = True
            self.__static_folder = static_folder
            self.__static_url = static_url

        for path, pipes in self.__paths.items():
            self.__map.add(Rule(path, endpoint=pipes))

        run_simple(host, port, self, *args, **kwargs)


app = App()
