import json
from datetime import datetime

from werkzeug.wrappers import BaseRequest, BaseResponse, CommonRequestDescriptorsMixin, \
    CommonResponseDescriptorsMixin
from werkzeug.wrappers.json import JSONMixin


class PipeRequest(BaseRequest, JSONMixin, CommonRequestDescriptorsMixin):
    pass


class PipeResponse(BaseResponse, JSONMixin, CommonResponseDescriptorsMixin):
    pass


def make_response(data, is_json: bool = False, *args, **kwargs) -> PipeResponse:
    """Makes WSGI Response from `data` argument

    :param data: Response data
    :return: WSGI Response
    :rtype: Response
    """
    if is_json:
        data = json.dumps(data, cls=PipeJsonEncoder)
        return PipeResponse(data, content_type='application/json', *args, **kwargs)
    else:
        return PipeResponse(data, *args, **kwargs)


class PipeJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return str(obj)
