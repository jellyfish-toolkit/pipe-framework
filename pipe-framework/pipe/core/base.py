import typing as t

from pipe.core import base
from pipe.core.data import DataObject, PipeException
from pipe.core.interface import Runnable


class Extractor(Runnable):
    """Abstract class for Extractors.
    Contains extract method which should be implemented by developer.

    Main goal - get the data and pass it next. Can use data_object
    with initial parameters, and can validate input [in development]

    :raises: NotImplementedError

    """
    def extract(self, data_object: DataObject) -> DataObject:
        raise NotImplementedError

    def run(self, data_object: DataObject):
        """Interface implementation

        :param data_object: data object passed from pipe

        """
        return self.extract(data_object)


class Transformer(Runnable):
    """Abstract class for Transformers.
    Contains transform method which should be implemented by developer.

    Main goal - get the data, transform it and pass it next.

    :raises: NotImplementedError

    """
    def transform(self, data_object: DataObject) -> DataObject:
        raise NotImplementedError

    def run(self, data_object: DataObject):
        """Interface implementation

        :param data_object: data object passed from pipe
        :type data_object: DataObject

        """
        return self.transform(data_object)


class Loader(Runnable):
    """Abstract class for Loader.
    Contains load method which should be implemented by developer.

    Main goal - get prepared data and put it to the view or storage.

    :raises: NotImplementedError

    """
    def load(self, data_object: DataObject):
        raise NotImplementedError

    def run(self, data_object: DataObject):
        """Interface implementation

        :param data_object: data object passed from pipe
        :type data_object: DataObject

        """
        return self.load(data_object)


class Pipe():
    """Main structure in the framework. Represent pipe through which all data pass.

    Pipe structure. Contains two parts - pipe for request
    and pipe for response.
    Data goes in next way
    request -> request extractor -> request transformer -> request loader ->
    response extractor -> response transformer -> response loader

    """

    # pipe structure
    request_pipe: t.Iterable[Runnable] = ()
    response_pipe: t.Iterable[Runnable] = ()

    def __init__(self, request):
        self.__request = request
        self.__shared_data_object: DataObject = DataObject(data=None)

    @property
    def data_object(self) -> DataObject:
        """Getter for inner data object

        """
        return self.__shared_data_object

    @data_object.setter
    def data_object(self, data_object: DataObject):
        """Setter for data object

        :param data_object:
        :type data_object: DataObject

        """
        self.__shared_data_object = DataObject(data_object.data)

    @property
    def request(self):
        """Getter for request object

        """
        return self.__request

    def run_pipe(self):
        """The main method.
        Takes data and pass through pipe. Handles request and response

        :raises: PipeException

        """

        self.data_object = DataObject(data={'request': self.request})

        self.__run_pipe(self.request_pipe, response=False)
        result = self.__run_pipe(self.response_pipe, response=True)

        return result

    def __run_pipe(self, inner_pipe: t.Iterable[Runnable],
                   response: bool) -> t.Union[None, t.Any]:

        result = None

        for item in inner_pipe:
            if issubclass(item.__class__, base.Extractor
                          ) or issubclass(item.__class__, base.Transformer):

                result = item.run(self.data_object)

                if result is None or not issubclass(
                    DataObject, result.__class__
                ):
                    raise PipeException(
                        "Transformer and Extractor should always return a DataObject"  # noqa: E501
                    )
                else:
                    self.data_object = result

            if issubclass(item.__class__, base.Loader) and response:
                result = item.run(self.data_object)

        return result

    def __str__(self):
        return self.__class__.__name__
