import json
from datetime import datetime

from frozendict import frozendict
from werkzeug.wrappers import BaseRequest, BaseResponse, CommonRequestDescriptorsMixin, CommonResponseDescriptorsMixin
from werkzeug.wrappers.json import JSONMixin


class PipeRequest(BaseRequest, JSONMixin, CommonRequestDescriptorsMixin):
    pass


class PipeResponse(BaseResponse, JSONMixin, CommonResponseDescriptorsMixin):
    pass


def make_response(store: frozendict, is_json: bool = False, *args, **kwargs) -> PipeResponse:
    """Makes WSGI Response from DataObject

    :param store: Store with response data
    :type store: Store
    :return: WSGI Response
    :rtype: Response
    """
    if is_json:
        data = json.dumps(store, cls=PipeJsonEncoder)
        return PipeResponse(data, content_type='application/json', *args, **kwargs)
    else:
        return PipeResponse(store, *args, **kwargs)


class PipeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)