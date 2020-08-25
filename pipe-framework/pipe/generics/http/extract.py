import valideer
from frozendict import frozendict
from pipe.core.base import Extractor
from pipe.core.decorators import validate
from pipe.generics.http.exceptions import EFormDataException
from pipe.server.wrappers import PipeRequest


@validate({
    '+{request_field}': valideer.Type(PipeRequest)
})
class EFormData(Extractor):
    """
    Generic extractor for form data from PipeRequest
    """
    request_field = 'request'
    method: str = 'POST'

    def extract(self, store: frozendict):
        request = store.get(self.request_field)
        if request.method != self.method:
            raise EFormDataException("Invalid request method")
        store = store.copy(**{'form': dict(request.form)})
        return store


@validate({
    '+{request_field}': valideer.Type(PipeRequest)
})
class EQueryStringData(Extractor):
    """
    Generic extractor for data from query string which you can find after ? sign in URL
    """
    request_field = 'request'

    def extract(self, store: frozendict):
        request = store.get('request')
        store = store.copy(**request.args)
        return store


@validate({
    '+{request_field}': valideer.Type(PipeRequest)
})
class EJsonBody(Extractor):
    """
    Generic extractor for data which came in JSON format
    """
    request_field = 'request'

    def extract(self, store: frozendict):
        request = store.get('request')
        store = store.copy(**{'json': request.json})
        return store
