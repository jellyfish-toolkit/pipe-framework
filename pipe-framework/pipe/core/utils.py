import json
import typing as t
from dataclasses import dataclass, field
from datetime import datetime

from pipe.core import PipeResponse
from pipe.core.base import Pipe
from pipe.core.data import Store


class PipeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)


@dataclass
class PipeList:
    """Replacement for built-in list, provides making a string from list of Pipes for storing list of Pipes in Werkzeug Map as endpoint

    """

    __pipes: list = field(default_factory=list)

    def add(self, pipe: Pipe) -> t.List[Pipe]:
        """Add pipe to the list

        :param pipe:
        :type pipe: Pipe
        :return: pipe list
        :rtype: t.List[Pipe]
        """
        self.__pipes.append(pipe)

        return self.__pipes

    def get_pipes(self) -> t.List[Pipe]:
        """Get all pipes

        :rtype: t.List[Pipe]
        """
        return self.__pipes

    def __str__(self):
        return '_'.join([str(pipe) for pipe in self.__pipes])

    def __hash__(self):
        return hash(self.__str__())


def make_response(store: Store, is_json=False, *args, **kwargs) -> PipeResponse:
    """Makes WSGI Response from DataObject

    :param store: Store with response data
    :type store: Store
    :return: WSGI Response
    :rtype: Response
    """
    if is_json:
        data = json.dumps(store.data, cls=PipeJsonEncoder)
        return PipeResponse(data, content_type='application/json', *args, **kwargs)
    else:
        return PipeResponse(store.data, *args, **kwargs)


class SingletonMeta(type):
    __instance: t.Optional[object] = None

    def __call__(cls, **options):
        if cls.__instance is None:
            cls.__instance = cls(**options)

        return cls.__instance


def configure(config):
    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            for key, value in config.items():
                setattr(wrapped, key, value)

            return wrapped(*args, **kwargs)

        return wrapper

    return decorator
