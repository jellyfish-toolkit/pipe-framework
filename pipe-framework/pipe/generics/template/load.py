import typing as t

import jinja2
from werkzeug.wrappers import Response

from pipe.core.base import Loader
from pipe.core.data import Store
from pipe.core.utils import make_response


class LTemplateResponseBase(Loader):
    context_field: str = 'context'
    template_folder: t.Optional[str] = None
    template_name: t.Optional[str] = None

    def get_template_folder(self) -> t.Optional[str]:
        """get_template_folder

        :return: String path to the folder
        :rtype: t.Optional[str]
        """
        return self.template_folder

    def get_template_name(self) -> t.Optional[str]:
        """get_template_name

        :return: String name of the template file
        :rtype: [type]
        """
        return self.template_name

    def get_context_field(self) -> str:
        """get_context_field

        :return: Field in DataObject where context for the template can be found
        :rtype: str
        """
        return self.context_field


class LJinja2TemplateResponseBase(LTemplateResponseBase):

    def __init__(self, *args, **options):
        """Setting Jinja2 environment

        you can provide any options you can find in Jinja2 documentation.

        By default we setting only loader and autoescape, but you can rewrite it too.
        """

        loader = options.get('loader', jinja2.FileSystemLoader(self.template_folder))
        autoescape = options.get('autoescape', jinja2.select_autoescape(['html', 'xml']))
        self.environ = jinja2.Environment(loader=loader, autoescape=autoescape, **options)

    def load(self, store: Store) -> Response:
        """load

        :param store: Store from Pipe
        :type store: Store
        :return: Werkzeug Response with template
        :rtype: Response
        """
        context = store.get(self.get_context_field(), {})
        template = self.environ.get_template(self.get_template_name())

        status = store.get('status', 200)
        rendered_template = Store(data=template.render(**context))

        return make_response(rendered_template, status=status, content_type='text/html')
