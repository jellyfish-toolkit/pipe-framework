import os
import sys

sys.path.insert(0, os.path.abspath('../../pipe-framework'))
from recommonmark.transform import AutoStructify

source_suffix = {
    '.md': 'markdown',
}

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosectionlabel', 'recommonmark', 'sphinx.ext.viewcode']

master_doc = 'index'

github_doc_root = 'https://github.com/jellyocean/pipe-framework/tree/master/docs/api/'

html_theme_options = {
    'nosidebar': True
}

def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
    }, True)
    app.add_transform(AutoStructify)
