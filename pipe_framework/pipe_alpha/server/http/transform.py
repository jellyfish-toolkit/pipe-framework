import typing as t
from collections import defaultdict
from dataclasses import dataclass

import valideer
from frozendict import frozendict
from pipe.core.base import Step


@dataclass
class TJsonResponseReady(Step):
    """Converts object from a 'data_field' for a simpliest API
    representation."""

    required_fields = {"+{data_field}": valideer.Type((dict, list))}

    data_field: str

    def transform(self, store: frozendict) -> frozendict:
        response_data: t.Union[list, dict] = store.get(self.data_field)

        result: defaultdict = defaultdict()

        if isinstance(response_data, list):
            result["count"] = len(response_data)
            result["data"] = response_data
        else:
            result = response_data

        store = store.copy(**{"response": result})

        return store
