import typing as t
from dataclasses import dataclass

from frozendict import frozendict
from pipe.core.base import Step


@dataclass
class TPutDefaults(Step):
    """
    Helper transformers, which puts values from `defaults` into `Store`, to specific `field_name`
    """
    defaults: dict
    field_name: str

    def transform(self, store: frozendict) -> frozendict:
        return store.copy(**{self.field_name: dict(**self.defaults, **store.get(self.field_name))})


@dataclass
class TLambda(Step):
    """
    Step for small transformations of a store. Useful for cases where writing specific step is an overengineering
    """
    lambda_: t.Optional[t.Callable] = None

    def transform(self, store: frozendict) -> frozendict:
        return self.lambda_(store)
