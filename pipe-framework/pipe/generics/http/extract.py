from werkzeug.wrappers import Request

from pipe.core.base import Extractor, ExtractorException
from pipe.core.data import Store


class EFormDataException(ExtractorException):
    pass


class EFormData(Extractor):
    """
    Generic extractor for form data from PipeRequest
    """
    method: str = 'POST'

    required_fields = {'request': {
        'type': 'object'
    }}

    save_validated: bool = True

    def extract(self, store: Store):
        result = store.copy()

        request = self.validated_data.get('request')

        if request.method != self.method:
            raise EFormDataException("Invalid request method")

        result.update({'form': dict(request.form)})

        return Store(data=result)


class EQueryStringData(Extractor):
    """
    Generic extractor for data from query string which you can find after ? sign in URL
    """
    required_fields = {'request': {
        'type': 'object'
    }}

    save_validated: bool = True

    def extract(self, store: Store):
        result = store.copy()

        request = self.validated_data.get('request')

        result.update(request.args)

        return Store(data=result)


class EJsonBody(Extractor):
    required_fields = {'request': {
        'type': 'object'
    }}

    def extract(self, store: Store):
        result = store.copy()

        request = store.get('request')

        result.update({'json': request.json})

        return Store(data=result)
