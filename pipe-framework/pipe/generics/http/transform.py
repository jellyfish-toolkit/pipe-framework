import typing as t
from collections import defaultdict
from dataclasses import dataclass, field

import valideer
from frozendict import frozendict

from pipe.core.base import Transformer
from pipe.core.decorators import validate


@validate({
    '+{data_field}': valideer.Type(t.Union[t.Dict, t.List])
})
@dataclass
class TJsonResponseReady(Transformer):
    """
    Converts object from a 'data_field' for a simpliest API representation
    """
    data_field: t.Union[t.Dict, t.List]

    def transform(self, store: frozendict) -> frozendict:
        response_data = store.get(self.data_field)

        result = defaultdict()

        if isinstance(response_data, list):
            result['count'] = len(response_data)
            result['data'] = response_data
        else:
            result = response_data

        store = store.copy(**{'response': result})

        return store
