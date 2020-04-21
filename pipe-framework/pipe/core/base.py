import typing as t
from rich.console import Console

from pipe.core import PipeResponse
from pipe.core.mixins import Runnable, ValidatableMixin
from pipe.core.data import PipeException, Store


class ExtractorException(Exception):
    pass


class Step(ValidatableMixin, Runnable):
    pass


class Extractor(Step):
    """Abstract class for Extractors.
    Contains extract method which should be implemented by developer.

    Main goal - get the data and pass it next. Can use store
    with initial parameters, and can validate input [in development]

    :raises: NotImplementedError
    """

    def extract(self, store: Store):
        pass

    def run(self, store: Store):
        return self.extract(store)


class Transformer(Step):
    """Abstract class for Transformers.
    Contains transform method which should be implemented by developer.

    Main goal - get the data, transform it and pass it next.

    :raises: NotImplementedError
    """

    def transform(self, store: Store):
        pass

    def run(self, store: Store):
        return self.transform(store)


class Loader(Step):
    """Abstract class for Loader.
    Contains load method which should be implemented by developer.

    Main goal - get prepared data and put it to the view or storage.

    :raises: NotImplementedError
    """

    def load(self, store: Store):
        pass

    def run(self, store: Store):
        return self.load(store)


class Pipe:
    """Main structure in the framework. Represent pipe through which all data pass.

    Pipe structure. Contains two parts - pipe for request
    and pipe for response.
    Data goes in next way
    request -> request extractor -> request transformer -> request loader ->
    response extractor -> response transformer -> response loader

    """

    pipe_schema: t.Dict[str, t.Dict[str, t.Iterable[Step]]] = {}
    __inspection_mode: bool = False

    def __init__(self, request, values, inspection, store_class=Store):
        self.__request = request
        self.__store_class = store_class
        self.__inspection_mode = inspection
        self.__shared_store: t.Optional[Store] = self.__store_class(values)

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

    def __print_step(self, step: Step, store: Store):
        console = Console()

        console.log('Current step is -> ', step.__class__.__name__, f'({step.__module__})')
        console.log('----------------------------------------------------------------')
        console.log(f'''{step.__class__.__name__} store state -> 
        ''', store.data)
        console.log('----------------------------------------------------------------')

    def run_pipe(self):
        """The main method.
        Takes data and pass through pipe. Handles request and response

        :raises: PipeException

        """

        self.store = self.store.extend(self.__store_class({'request': self.request}))

        pipe_to_run = self.pipe_schema.get(self.request.method, {'in': (), 'out': ()})

        self.__run_pipe(pipe_to_run.get('in', ()), response=False)
        result = self.__run_pipe(pipe_to_run.get('out', ()), response=True)

        return result

    def __run_pipe(self, inner_pipe: t.Iterable[t.Union[Step]], response: bool) -> t.Union[
        None, t.Any]:

        result = None

        for item in inner_pipe:

            if self.__inspection_mode:
                self.__print_step(item, self.store)

            if issubclass(item.__class__, Extractor) or issubclass(item.__class__, Transformer):

                item.validate(self.store)
                result = item.run(self.store)

                if result is None or not issubclass(Store, result.__class__):
                    raise PipeException("Transformer and Extractor should always return a Store"  # noqa: E501
                                        )
                else:
                    self.store = result

            if issubclass(item.__class__, Loader) and response:
                item.validate(self.store)
                result = item.run(self.store)

                if issubclass(result.__class__, PipeResponse) or isinstance(result, PipeResponse):
                    return result

                if issubclass(result.__class__, Store):
                    self.store = result

        return result

    def __str__(self):
        return self.__class__.__name__
