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

    required_fields = {'+{data_field}': valideer.Type((list, dict))}

    data_field: str = 'response'
    status: int = 200

    def load(self, store: frozendict):
        return make_response(store.get(self.data_field), is_json=True, status=self.status)


@dataclass
class LResponse(Loader):
    """
    Sends plain response from datafield, with status from field status
    """

    required_fields = {
        '+{data_field}': valideer.Type((str, list, dict)),
        '{status_field}': valideer.Type(int),
    }

    data_field: str = 'response'
    status_field: str = 'status'
    headers: dict = None
    status = None

    def load(self, store: frozendict):
        if self.status is None:
            self.status = store.get(self.status_field, 200)

        return make_response(store.get(self.data_field), status=self.status, headers=self.headers)


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
