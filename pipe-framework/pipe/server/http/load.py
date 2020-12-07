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
        '+{data_field}': valideer.Type(list, dict)
    }

    data_field: str = 'response'
    status: int = 200

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), is_json=True,
                             status=self.status)


@dataclass
class LResponse(Loader):
    """
    Sends plain response from datafield, with status from field status
    """

    required_fields = {
        '+{data_field}': valideer.Type(str, list, dict)
    }

    data_field: str = 'response'
    status: int = 200

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), status=self.status)


class LNotFound(Loader):
    def load(self, store: frozendict):
        return make_response(f'object not found: {store.get("exception")}', status=404)


class LServerError(Loader):
    def load(self, store: frozendict):
        return make_response(f'server error: {store.get("exception")}', status=500)


class LUnauthorized(Loader):
    def load(self, store: frozendict):
        return make_response(f'unauthorized: {store.get("exception")}', status=401)


class LBadRequest(Loader):
    def load(self, store: frozendict):
        return make_response(f'bad request: {store.get("exception")}', status=400)
