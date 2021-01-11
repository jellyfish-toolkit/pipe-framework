import valideer
from frozendict import frozendict
from pipe.core.base import Extractor
from pipe.core.exceptions import ExtractorException
from pipe.server.http.exceptions import EFormDataException
from pipe.server.wrappers import PipeRequest


class EFormData(Extractor):
    """
    Generic extractor for form data from PipeRequest
    """
    required_fields = {'+{request_field}': valideer.Type(PipeRequest)}

    request_field = 'request'
    method: str = 'POST'

    def extract(self, store: frozendict):
        request = store.get(self.request_field)
        if request.method != self.method:
            raise EFormDataException("Invalid request method")
        store = store.copy(**{'form': dict(request.form)})
        return store


class EQueryStringData(Extractor):
    """
    Generic extractor for data from query string which you can find after ? sign in URL
    """
    required_fields = {'+{request_field}': valideer.Type(PipeRequest)}

    request_field = 'request'

    def extract(self, store: frozendict):
        request = store.get('request')
        store = store.copy(**request.args)
        return store


class EJsonBody(Extractor):
    """
    Generic extractor for data which came in JSON format
    """
    required_fields = {'+{request_field}': valideer.Type(PipeRequest)}

    request_field = 'request'

    def extract(self, store: frozendict):
        request = store.get('request')

        if request.json is None:
            raise ExtractorException('JSON is missing from request')

        store = store.copy(**{'json': request.json})
        return store
