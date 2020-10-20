import typing as t
from dataclasses import dataclass

import valideer
from frozendict import frozendict

from pipe.core.base import Loader
from pipe.server.wrappers import make_response


@dataclass
class LJsonResponse(Loader):
    """
    Creates JSON response from field in 'data_field' property
    """

    required_fields = {
        '+{data_field}': valideer.Type(t.Union[t.Dict, t.List])
    }

    data_field = 'response'
    status_field = 'status'

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), is_json=True,
                             status=store.get(self.status_field, 200))


@dataclass
class LResponse(Loader):
    """
    Sends plain response from datafield, with status from field status
    """

    required_fields = {
        '+{data_field}': valideer.Type(t.Union[t.Dict, t.List])
    }

    data_field = 'response'
    status_field = 'status'

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), status=store.get(self.status_field, 200))


class LNotFound(Loader):
    def load(self, store: frozendict):
        return make_response('object not found', status=404)


class LServerError(Loader):
    def load(self, store: frozendict):
        return make_response('server error', status=500)


class LUnauthorized(Loader):
    def load(self, store: frozendict):
        return make_response('unauthorized', status=401)


class LBadRequest(Loader):
    def load(self, store: frozendict):
        return make_response('bad request', status=400)
