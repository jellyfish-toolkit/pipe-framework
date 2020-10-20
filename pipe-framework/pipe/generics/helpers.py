from dataclasses import dataclass

from frozendict import frozendict

from pipe.core.base import Transformer


@dataclass
class TPutDefaults(Transformer):
        """
        Helper transformers, which puts values from defaults into Store
        """
        defaults: dict
        field_name: str

        def transform(self, store: frozendict) -> frozendict:
            return store.copy(**{
                self.field_name: self.defaults
            })
