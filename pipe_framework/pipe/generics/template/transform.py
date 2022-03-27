import typing as t

import jinja2
import valideer as V
from frozendict import frozendict
from pipe.core.base import Step


class TTemplateResponseReady(Step):
    required_fields = {"+{context_field}": V.Type((str, dict))}

    context_field: str = "context"
    template_folder: t.Optional[str] = None
    template_name: t.Optional[str] = None

    def __init__(self, template_name="", **options):
        """Setting Jinja2 environment you can provide any options you can find
        in Jinja2 documentation.

        By default we setting only loader and autoescape, but you can
        rewrite it too.
        """

        loader = options.get("loader", jinja2.FileSystemLoader(self.template_folder))
        autoescape = options.get(
            "autoescape", jinja2.select_autoescape(["html", "xml"])
        )

        self.environ = jinja2.Environment(
            loader=loader, autoescape=autoescape, **options
        )
        self.template_name = template_name

    def transform(self, store: frozendict) -> frozendict:
        context = store.get(self.context_field, {})
        template = self.environ.get_template(self.template_name)

        status = store.get("status", 200)
        return frozendict(template=template.render(**context), status=status)
