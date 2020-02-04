import abc

from pipe.core.data import DataObject


class Runnable(abc.ABC):
    """Interface for every pipe element.
    Loader, Transformer and Extractor should implement
    run method to easily go through pipe.

    """
    @abc.abstractmethod
    def run(self, data_object: DataObject):
        """Method to implement. Takes data object, cause directly participate in
        piping process

        :param data_object:
        :type data: DataObject
        """
        pass
