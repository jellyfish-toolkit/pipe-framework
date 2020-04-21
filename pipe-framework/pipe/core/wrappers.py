from werkzeug.wrappers import BaseRequest, BaseResponse
from werkzeug.wrappers.json import JSONMixin


class PipeRequest(BaseRequest, JSONMixin):
    pass


class PipeResponse(BaseResponse, JSONMixin):
    pass