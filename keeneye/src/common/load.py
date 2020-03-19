import typing as t
import os
import string

from pipe.core.base import Loader
from pipe.core.data import Store
from pipe.core.utils import make_response
from pipe.generics.template.load import LJinja2TemplateResponseBase
from oauth2client.service_account import ServiceAccountCredentials
import gspread


class LTemplateResponse(LJinja2TemplateResponseBase):
    template_folder = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'templates')

    def __init__(self, template_name: str = 'index.html', *args, **kwargs):
        self.template_name = template_name

        super().__init__(*args, **kwargs)


class LGoogleSheets(Loader):
    credentials_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'static', 'resources', 'cred.json')

    required_fields = {
        'spreadsheet': dict,
        'user': object
    }
    save_validated: bool = True

    def __init__(self, *args, **kwargs):
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        self.gc = gspread.authorize(credentials)

        super().__init__(*args, **kwargs)

    def load(self, store: Store) -> Store:
        user = self.validated_data.get('user', {})

        spreadsheet = self.gc.create('Estimating score - {}'.format(user.displayName))
        worksheet = spreadsheet.sheet1

        for key, values in store.get('spreadsheet').get('rows').items():
            worksheet.append_row(
                values=values,
                table_range=key
            )

        for email in map(lambda email: email.replace(' ', ''), store.get('emails-to-share').split(',')):
            spreadsheet.share(email, 'user', 'writer')

        result = {
            'doc_url': f'https://docs.google.com/spreadsheets/d/{spreadsheet.id}'
        }

        return Store(data=result)


class LKeenEyeLinkResponse(Loader):
    required_fields = {
        'doc_url': str
    }

    def load(self, store: Store):
        url = self.validated_data.get('doc_url')

        return make_response(Store(url))
