from abc import ABC, abstractmethod

from frozendict import frozendict


class RunnableException(Exception):
    pass


class Runnable(ABC):
    """Interface for every pipe element.
    Loader, Transformer and Extractor should implement
    run method to easily go through pipe.
    """

    @abstractmethod
    def run(self, store: frozendict):
        """Method to implement. Takes data object, cause directly participate in
        piping process

        :param store:
        :type data: Store
        """
        pass
