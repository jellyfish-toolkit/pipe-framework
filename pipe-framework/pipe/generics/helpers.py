from dataclasses import dataclass
from typing import Optional

from pipe.core.base import Transformer
from pipe.core.data import Store


@dataclass
class TPutDefaults(Transformer):

        defaults: dict
        field_name: str

        def transform(self, store: Store) -> Store:

            field = store.get(self.field_name)
            field.update(self.defaults)

            return Store(data=field)
