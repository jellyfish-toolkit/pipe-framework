from werkzeug.wrappers import Request

from pipe.core.base import Extractor, ExtractorException
from pipe.core.data import Store


class EFormDataException(ExtractorException):
    pass


class EFormData(Extractor):
    method: str = 'POST'

    required_fields = {'request': Request}

    save_validated: bool = True

    def extract(self, store: Store):

        request = self.validated_data.get('request')

        if request.method != self.method:
            raise EFormDataException("Invalid request method")

        result = {'form': dict(request.form)}
        result.update(store.data)

        return Store(data=result)


class EUrlData(Extractor):
    required_fields = {'request': Request}

    save_validated: bool = True

    def extract(self, store: Store):

        request = self.validated_data.get('request')

        result = {'args': dict(request.args)}
        result.update(store.data)

        return Store(data=result)
