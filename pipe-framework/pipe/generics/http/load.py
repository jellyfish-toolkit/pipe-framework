import typing as t
from dataclasses import dataclass

import valideer
from frozendict import frozendict

from pipe.core.base import Loader
from pipe.core.decorators import validate
from pipe.server.wrappers import make_response


@validate({
    '+{data_field}': valideer.Type(t.Union[t.Dict, t.List])
})
@dataclass
class LJsonResponse(Loader):
    """
    Creates JSON response from field in 'data_field' property
    """
    data_field = 'response'
    status_field = 'status'

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), is_json=True,
                             status=store.get(self.status_field, 200))


@validate({
    '+{data_field}': valideer.Type(t.Union[t.Dict, t.List])
})
@dataclass
class LResponse(Loader):
    """
    Sends plain response from datafield, with status from field status
    """
    data_field = 'response'
    status_field = 'status'

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), status=store.get(self.status_field, 200))
