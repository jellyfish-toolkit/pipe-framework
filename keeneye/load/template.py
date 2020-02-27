import os
from pipe.generics.template.load import Jinja2TemplateLoaderBase


class TemplateLoader(Jinja2TemplateLoaderBase):
    template_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'templates')

    def __init__(self, template_name: str = 'index.html', *args, **kwargs):
        self.template_name = template_name

        super().__init__(*args, **kwargs)

