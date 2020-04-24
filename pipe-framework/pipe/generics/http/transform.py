import typing as t
from dataclasses import dataclass, field

from pipe.core.base import Transformer
from pipe.core.data import Store


@dataclass
class TJsonResponseReady(Transformer):
    """
    Converts object from a 'data_field' for a simpliest API representation
    """
    data_field: t.Optional[str] = None
    response_template: dict = field(default_factory=dict)

    def transform(self, store: Store) -> Store:
        self.required_fields = {
            self.data_field: {
                'type': 'object'
            }
        }
        self.validate(store)

        data = store.data.copy()

        response_data = data.get(self.data_field)

        result = self.response_template.copy()

        if isinstance(response_data, list):
            result['count'] = len(response_data)
            result['data'] = response_data
        else:
            result = response_data

        data.update({'response': result})

        return Store(data)
