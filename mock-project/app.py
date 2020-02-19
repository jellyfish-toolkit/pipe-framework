import os
import pipe.core as core
import pipe.generics as generics


class TemplateLoaderBase(generics.load.Jinja2TemplateLoaderBase):
    template_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   'templates')


class TemplateLoaderIndex(TemplateLoaderBase):
    template_name = 'subfolder/index.html'


class ContextExtractor(core.base.Extractor):

    def extract(self,
                store: core.data.Store) -> core.data.Store:

        context = {
            'small': store.get('small', 'Not found'),
            'piece': 'Hi',
            'of': 'I\'m building a context here',
            'context': 'Here it is'
        }

        return core.data.Store(data={
            'context': context
        })


@core.app.path('/')
class MainPipe(core.base.Pipe):
    response_pipe = [ContextExtractor(), TemplateLoaderIndex()]


if __name__ == '__main__':
    core.app.run(host='127.0.0.1', port=8080, use_debugger=True)
