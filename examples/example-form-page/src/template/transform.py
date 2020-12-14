import os
from dataclasses import dataclass

from frozendict import frozendict

from pipe.core.base import Transformer
from pipe.generics.template.transform import TJinja2TemplateResponseReady


class TTemplateResponseReady(TJinja2TemplateResponseReady):
    template_folder = os.path.join(os.path.dirname(__file__), 'templates')
