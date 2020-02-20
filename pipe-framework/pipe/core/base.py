import typing as t

from schema import Schema

from pipe.core import base
from pipe.core.data import PipeException, Store
from pipe.core.interface import Runnable


class ValidatableMixin():

    schema: dict = {}
    errors: t.Optional[list] = None

    def validate(self, store: Store, ignore_extra_keys: bool = True):
        current_schema = Schema(
            self.schema, ignore_extra_keys=ignore_extra_keys
        )
        result = current_schema.validate(store.data)

        return result


class Extractor(Runnable, ValidatableMixin):
    """Abstract class for Extractors.
    Contains extract method which should be implemented by developer.

    Main goal - get the data and pass it next. Can use store
    with initial parameters, and can validate input [in development]

    :raises: NotImplementedError

    """
    def extract(self, store: Store) -> Store:
        raise NotImplementedError

    def run(self, store: Store):
        """Interface implementation

        :param store: data object passed from pipe

        """
        return self.extract(store)


class Transformer(Runnable, ValidatableMixin):
    """Abstract class for Transformers.
    Contains transform method which should be implemented by developer.

    Main goal - get the data, transform it and pass it next.

    :raises: NotImplementedError

    """
    def transform(self, store: Store) -> Store:
        raise NotImplementedError

    def run(self, store: Store):
        """Interface implementation

        :param store: data object passed from pipe
        :type store: DataObject

        """
        return self.transform(store)


class Loader(Runnable, ValidatableMixin):
    """Abstract class for Loader.
    Contains load method which should be implemented by developer.

    Main goal - get prepared data and put it to the view or storage.

    :raises: NotImplementedError

    """
    def load(self, store: Store):
        raise NotImplementedError

    def run(self, store: Store):
        """Interface implementation

        :param store: data object passed from pipe
        :type store: DataObject

        """
        return self.load(store)


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

    def __init__(self, request, store_class=Store):
        self.__request = request
        self.__store_class = store_class
        self.__shared_store: Store = self.__store_class(None)

    @property
    def store(self) -> Store:
        """Getter for inner data object

        """
        return self.__shared_store

    @store.setter
    def store(self, store: Store):
        """Setter for data object

        :param store:
        :type store: Store

        """
        self.__shared_store = self.__store_class(store.data)

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

        self.store = self.__store_class({'request': self.request})

        self.__run_pipe(self.request_pipe, response=False)
        result = self.__run_pipe(self.response_pipe, response=True)

        return result

    def __run_pipe(self, inner_pipe: t.Iterable[Runnable],
                   response: bool) -> t.Union[None, t.Any]:

        result = None

        for item in inner_pipe:
            if issubclass(item.__class__, base.Extractor
                          ) or issubclass(item.__class__, base.Transformer):

                validated_store = item.validate(self.store)
                result = item.run(validated_store)

                if result is None or not issubclass(Store, result.__class__):
                    raise PipeException(
                        "Transformer and Extractor should always return a Store"  # noqa: E501
                    )
                else:
                    self.store = result

            if issubclass(item.__class__, base.Loader) and response:
                result = item.run(self.store)

        return result

    def __str__(self):
        return self.__class__.__name__
