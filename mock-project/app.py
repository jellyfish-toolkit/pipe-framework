import os
import pipe.core as core
import pipe.generics as generics


class BaseTemplateLoader(generics.load.Jinja2TemplateLoaderBase):
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'templates')


class IndexTemplateLoader(BaseTemplateLoader):
    template_name = 'index.html'


class ContextExtractor(core.base.Extractor):

    def extract(self,
                data_object: core.data.DataObject) -> core.data.DataObject:

        context = {
            'small': data_object.data.get('small', 'Not found'),
            'piece': 'Hi',
            'of': 'I\'m building a context here',
            'context': 'Here it is'
        }

        return core.data.DataObject(data={
            'context': context
        })


@core.app.path('/')
class MainPipe(core.base.Pipe):
    response_pipe = [ContextExtractor(), IndexTemplateLoader()]


if __name__ == '__main__':
    core.app.run(host='127.0.0.1', port=8080, use_debugger=True)
