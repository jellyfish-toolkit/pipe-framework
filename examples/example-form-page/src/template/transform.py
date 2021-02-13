import os
from pipe.generics.template.transform import TTemplateResponseReady


class TTemplateResponseReady(TTemplateResponseReady):
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
