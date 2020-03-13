import os

from pipe.core import app
from pipe.core.base import Pipe
from pipe.generics.helpers import TPutDefaults
from pipe.generics.request.extract import EFormData

from src.common.load import LTemplateResponse
from src.jira.extract import EJiraIssues
from src.jira.transform import TCountPercents, TFromJiraToDict


@app.path('/')
class MainPipe(Pipe):
    pipe_schema = {
        'GET': {
            'out': (
                LTemplateResponse(template_name='index.html'),
            )
        },
        'POST': {
            'in': (
                EFormData(),
                TPutDefaults(defaults={
                    'base_url': 'https://jellyfishtech.atlassian.net',
                    'email': 'rlatyshenko.dev@gmail.com',
                    'api_key': 'Pc4YdcblApRoUPJOp6366310'
                },
                    field_name='form'),
            ),
            'out': (
                EJiraIssues(),
                TFromJiraToDict(),
                TCountPercents()
            )
        }
    }




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, use_debugger=True, use_reloader=True,
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
