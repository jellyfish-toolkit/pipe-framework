from werkzeug.wrappers import BaseRequest, BaseResponse, CommonRequestDescriptorsMixin, CommonResponseDescriptorsMixin
from werkzeug.wrappers.json import JSONMixin


class PipeRequest(BaseRequest, JSONMixin, CommonRequestDescriptorsMixin):
    pass


class PipeResponse(BaseResponse, JSONMixin, CommonResponseDescriptorsMixin):
    pass
