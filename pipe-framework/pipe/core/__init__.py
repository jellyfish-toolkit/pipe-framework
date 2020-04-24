"""WSGI App for http related Pipes

"""
import typing as t

from typeguard import typechecked
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from pipe.core.wrappers import PipeRequest, PipeResponse

import pipe.core.base as base
import pipe.core.data as data

__all__ = ['app', 'path']


class AppException(Exception):
    pass


@typechecked
class App:
    """Main WSGI app wrapper which run pipes according to request

    """

    paths: data.Store = data.Store({})

    __map: Map = Map()
    __static_serving: bool = False
    __static_folder: t.Optional[str] = None
    __static_url: t.Optional[str] = None
    __inspection_mode: bool = False

    def __init__(self):
        for path, pipes in self.paths.data.items():
            self.__map.add(Rule(path, endpoint=pipes))

    def wsgi_app(self, environ, start_response):
        """Main WSGI app, see werkzeug documentation for more

        """
        request = PipeRequest(environ)
        adapter = self.__map.bind_to_environ(environ)
        result = None

        try:
            endpoint, values = adapter.match()
        except HTTPException as e:
            return e(environ, start_response)

        for pipe in endpoint.get_pipes():
            result = pipe(request, values, self.__inspection_mode).run_pipe()

        if isinstance(result, PipeResponse):
            return result(environ, start_response)

        response = PipeResponse(status=204)

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

        :param static_folder: points to the folder with the static files, for serving
        :type static_folder: str, optional

        :param static_url: on what endpoint app should serve static files
        :type static_url: str

        :param use_inspection: Toggle on inspection mode of the framework
       :type use_inspection: bool
        """

        if static_folder is not None:
            self.__static_serving = True
            self.__static_folder = static_folder
            self.__static_url = static_url

        if kwargs.get('use_inspection', False):
            self.__inspection_mode = True
            del kwargs['use_inspection']

        run_simple(host, port, self, *args, **kwargs)


def path(route: str):
    """Decorator for adding pipe as a handler for a route

    :param route: Werkzeug formatted route
    :type route: string
    """

    def decorator(pipe):

        current_pipes = App.paths.get(route, None)

        if current_pipes is None:
            current_pipes = (pipe,)
        else:
            current_pipes = current_pipes + (pipe,)

        App.paths = App.paths.extend({route: current_pipes})

    return decorator

app = App()
