"""WSGI App for http related Pipes

"""
import typing as t

from frozendict import frozendict
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.serving import run_simple
from pipe.core.wrappers import PipeRequest, PipeResponse
from pipe.server.pipe import HTTPPipe


class AppException(Exception):
    pass


class App:
    """Main WSGI app wrapper which run pipes according to request

    """

    __map: Map = Map()
    __pipes: frozendict = frozendict()
    __static_serving: bool = False
    __static_folder: t.Optional[str] = None
    __static_url: t.Optional[str] = None
    __inspection_mode: bool = False

    def __make_endpoint(self, pipe: HTTPPipe):
        return pipe.__class__.__name__

    def route(self, route: str):
        """Decorator for adding pipe as a handler for a route

        :param route: Werkzeug formatted route
        :type route: string
        """

        def decorator(pipe):
            endpoint = self.__make_endpoint(pipe)
            if endpoint in self.__pipes:
                raise AppException(
                    'Route rewrites previously added route, please use hooks if you want to run '
                    'more then one pipe')

            self.__map.add(Rule(route, endpoint=endpoint))
            self.__pipes = self.__pipes.copy(**{
                endpoint: pipe
            })

        return decorator

    def wsgi_app(self, environ, start_response):
        """Main WSGI app, see werkzeug documentation for more

        """
        request = PipeRequest(environ)
        adapter = self.__map.bind_to_environ(environ)

        try:
            endpoint, values = adapter.match()
        except HTTPException as e:
            return e(environ, start_response)

        pipe = self.__pipes.get(endpoint)
        result = pipe(request, values, self.__inspection_mode).run_pipe()

        if isinstance(result, PipeResponse):
            return result(environ, start_response)

        response = PipeResponse(status=204)

        return response(environ, start_response)

    def __call__(self, environ, start_response):
        if self.__static_serving:
            app_with_static = SharedDataMiddleware(self.wsgi_app,
                                                   {self.__static_url: self.__static_folder})
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


app = App()
