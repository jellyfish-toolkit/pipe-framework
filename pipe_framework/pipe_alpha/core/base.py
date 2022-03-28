import re
import typing as t

import valideer as V
from frozendict import frozendict
from pipe.core.exceptions import StepExecutionException, StepValidationException
from rich.console import Console


class Step:
    """Base class providing basic functionality for all steps related classes."""

    _available_methods = ("extract", "transform", "load")

    # field for store validation schema
    required_fields: dict = {}

    def __and__(self, other: "Step") -> "Step":
        """Overriding boolean AND operation for merging steps"""

        def run(self, store: frozendict) -> frozendict:

            try:
                result_a = self.obj_a.run(store)
                result_b = self.obj_b.run(store)
            except Exception:
                return store

            return store.copy(**dict(obj_a=result_a, obj_b=result_b))

        return Step.factory(run, "AndStep", obj_a=self, obj_b=other)()

    def __or__(self, other: "Step") -> "Step":
        """Overriding boolean OR operation for merging steps:"""

        def run(self, store: frozendict) -> frozendict:

            try:
                result = self.obj_a.run(store)
            except Exception as e:
                store = store.copy(**{"exception": e})
                result = self.obj_b.run(store)

            return result

        return Step.factory(run, "OrStep", obj_a=self, obj_b=other)()

    def _parse_dynamic_fields(self) -> None:
        """Processes fields in validation config which should be taken from
        step instance."""
        dynamic_config = {}
        keys = list(self.required_fields.keys())

        for key in keys:
            if (key.startswith("+{") or key.startswith("{")) and key.endswith("}"):
                variable_name = re.sub(r"\{|\}", "", key)
                dynamic_config.update(
                    {
                        getattr(
                            self, variable_name.replace("+", "")
                        ): self.required_fields.get(key)
                    }
                )
                del self.required_fields[key]

        self.required_fields = dict(**self.required_fields, **dynamic_config)

    def validate(self, store: frozendict) -> frozendict:
        """Validates store according to `Step.required_fields` field."""
        self._parse_dynamic_fields()

        validator = V.parse(self.required_fields)
        try:
            adapted = validator.validate(store)
        except V.ValidationError as e:
            raise StepValidationException(
                f"Validation for step {self.__class__.__name__} \
                failed with error \n{e.message}"
            )

        return store.copy(**adapted)

    @classmethod
    def factory(cls, run_method: t.Callable, name: str = "", **arguments) -> type:
        """Step factory, creates step with `run_method` provided."""
        return type(name, (cls,), dict(run=run_method, **arguments))

    def run(self, store: frozendict) -> frozendict:
        """Method which provide ability to run any step."""

        if self.required_fields is not None:
            store = self.validate(store)

        for method in self._available_methods:
            if hasattr(self, method):
                return getattr(self, method)(store)

        raise StepExecutionException(
            f"You should define one of this methods \
            {','.join(self._available_methods)}"
        )


class BasePipe:
    """Base class for all pipes, implements running logic and inspection of
    pipe state on every step."""

    # Flag which show, should pipe print its state every step
    __inspection_mode: bool

    def __init__(self, initial: t.Mapping, inspection: bool = False):
        """:param initial: Initial store state."""
        self.__inspection_mode = inspection
        self.store = self.before_pipe(frozendict(initial))

    def set_inspection(self, enable: bool = True) -> bool:
        """Sets inspection mode."""
        self.__inspection_mode = enable

        return self.__inspection_mode

    @staticmethod
    def __print_step(step: Step, store: frozendict) -> None:
        """Prints passed step and store to the console."""
        console = Console()

        console.log(
            "Current step is -> ", step.__class__.__name__, f"({step.__module__})"
        )
        console.log(f"{step.__class__.__name__} STORE STATE")
        console.print(store.__dict__, overflow="fold")
        console.log("\n\n")

    def _run_pipe(self, pipe: t.Iterable[Step]) -> t.Union[None, t.Any]:
        """Protected method to run subpipe declared in schema (schema can be
        different depending on pipe type)
        """

        for item in pipe:

            if self.__inspection_mode:
                self.__print_step(item, self.store)

            intermediate_store = item.run(self.store)

            if self.interrupt(intermediate_store):
                return self.after_pipe(intermediate_store)

            self.store = intermediate_store

        return self.after_pipe(self.store)

    def before_pipe(self, store: frozendict) -> frozendict:
        """Hook for running custom pipe (or anything) before every pipe
        execution.
        """
        return store

    def after_pipe(self, store: frozendict) -> frozendict:
        """Hook for running custom pipe (or anything) after every pipe
        execution.
        """
        return store

    def interrupt(self, store: frozendict) -> bool:
        """Interruption hook which could be overridden, allow all subclassed
        pipes set one condition, which will be respected after any step was
        run. If method returns true, pipe will not be finished and will return
        value returned by step immediately (respects after_pipe hook)

        :param store: :return:
        """
        return False

    def __str__(self) -> str:
        return self.__class__.__name__


class NamedPipe(BasePipe):
    """Simple pipe structure to interact with named pipes."""

    pipe_schema: t.Dict[str, t.Iterable[Step]]

    def run_pipe(self, name: str):
        pipe_to_run = self.pipe_schema.get(name, ())
        return self._run_pipe(pipe_to_run)
