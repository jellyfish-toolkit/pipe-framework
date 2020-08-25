import typing as t
from abc import ABC, abstractmethod

from frozendict import frozendict
from rich.console import Console
from valideer import ValidationError

from pipe.core.exceptions import PipeException


class Step(ABC):

    @abstractmethod
    def run(self, store: frozendict):
        pass



class CombinedStep(ABC):
    def __init__(self, obj_a, obj_b):
        self.obj_a, self.obj_b = obj_a, obj_b

    @abstractmethod
    def run(self, store: frozendict):
        pass



class OrStep(CombinedStep):

    def run(self, store: frozendict):

        try:
            result = self.obj_a.run(store)
        except ValidationError:
            result = self.obj_b.run(store)

        return result


class Extractor(Step):
    """Abstract class for Extractors.
    Contains extract method which should be implemented by developer.

    Main goal - get the data and pass it next. Can use store
    with initial parameters, and can validate input [in development]

    :raises: NotImplementedError
    """

    def extract(self, store: frozendict):
        pass

    def run(self, store: frozendict):
        return self.extract(store)


class Transformer(Step):
    """Abstract class for Transformers.
    Contains transform method which should be implemented by developer.

    Main goal - get the data, transform it and pass it next.

    :raises: NotImplementedError
    """

    def transform(self, store: frozendict):
        pass

    def run(self, store: frozendict):
        return self.transform(store)


class Loader(Step):
    """Abstract class for Loader.
    Contains load method which should be implemented by developer.

    Main goal - get prepared data and put it to the view or storage.

    :raises: NotImplementedError
    """

    def load(self, store: frozendict):
        pass

    def run(self, store: frozendict):
        return self.load(store)


class BasePipe:
    __inspection_mode: bool

    def __init__(self, initial, inspection: bool = False):
        self.__inspection_mode = inspection
        self.store = frozendict(initial)

        self.before_pipe(self.store)

    def set_inspection(self, enable: bool = True):
        self.__inspection_mode = enable

    def __print_step(self, step: Step, store: frozendict):
        console = Console()

        console.log('Current step is -> ', step.__class__.__name__, f'({step.__module__})')
        console.log(f'{step.__class__.__name__} STORE STATE')
        console.log('----------------------------------------------------------------')
        console.log(store)
        console.log('----------------------------------------------------------------')
        console.log('\n\n')

    def _run_pipe(self, pipe: t.Iterable[Step]) -> t.Union[
        None, t.Any]:

        for item in pipe:

            if self.__inspection_mode:
                self.__print_step(item, self.store)

            if issubclass(item.__class__, Extractor) or issubclass(item.__class__, Transformer):
                result = item.run(self.store)

                if result is None or not issubclass(frozendict, result.__class__):
                    raise PipeException(
                        'Transformer and Extractor should always return a frozendict')  # noqa: E501
                else:
                    self.store = result

            if issubclass(item.__class__, Loader):
                result = item.run(self.store)

                if self.should_return(result):
                    self.after_pipe(self.store)
                    return result

                if issubclass(result.__class__, frozendict) or isinstance(result, frozendict):
                    self.store = result

        self.after_pipe(self.store)
        return self.store

    def before_pipe(self, store: t.Mapping) -> t.NoReturn:
        pass

    def after_pipe(self, stor: t.Mapping) -> t.NoReturn:
        pass

    def should_return(self, result: t.Mapping):
        return False

    def __str__(self):
        return self.__class__.__name__


class NamedPipe(BasePipe):
    pipe_schema: t.Dict[str, t.Iterable[Step]]

    def run_pipe(self, name: str):
        pipe_to_run = self.pipe_schema.get(name, ())
        return self._run_pipe(pipe_to_run)
