import abc

from pipe.core.data import Store


class Runnable(abc.ABC):
    """Interface for every pipe element.
    Loader, Transformer and Extractor should implement
    run method to easily go through pipe.

    """
    @abc.abstractmethod
    def run(self, store: Store):
        """Method to implement. Takes data object, cause directly participate in
        piping process

        :param store:
        :type data: Store
        """
        pass
