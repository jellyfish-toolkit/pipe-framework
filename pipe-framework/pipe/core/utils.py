import typing as t
from dataclasses import dataclass, field

from werkzeug.wrappers import Response

from pipe.core.base import Pipe
from pipe.core.data import Store


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


def make_response(store: Store, *args, **kwargs) -> Response:
    """Makes WSGI Response from DataObject

    :param store: Store with response data
    :type store: Store
    :return: WSGI Response
    :rtype: Response
    """

    # TODO: Ugly, change data to another name
    return Response(store.data, *args, **kwargs)


class Singleton():

    __instances: t.Dict = None

    @classmethod
    def instance(cls, name, **options):
        if cls.__instances.get(name, None) is None:
            cls.__instances.update({name: cls(**options)})

        return cls.__instances.get(name)
