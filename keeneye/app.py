import os

from pipe.core import app
from pipe.core.base import Pipe
from pipe.generics.request.extract import FormExtractor

from keeneye.load.template import TemplateLoader
from keeneye.extract.jira import JiraIssuesExtractor
from keeneye.transform.jira import PutDefaultsTransformer


@app.path('/')
class MainPipe(Pipe):
    pipe_schema = {
        'GET': {
            'out': (TemplateLoader(template_name='index.html'),)
        },
        'POST': {
            'in': (FormExtractor(), PutDefaultsTransformer(),), 'out': (JiraIssuesExtractor(),)
        }
    }


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, use_debugger=True, use_reloader=True,
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
