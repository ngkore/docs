import sys

sys.path.append('./')
from custom_conf import *

############################################################
### Extensions
############################################################

extensions = [
    'sphinx_design',
    'sphinx_tabs.tabs',
    'sphinx_reredirects',
    'youtube_links',
    'related_links',
    'custom_rst_roles',
    'terminal_output',
    'sphinx_copybutton',
    'sphinxext.opengraph',
    'myst_parser',
    'sphinxcontrib.jquery',
    'notfound.extension'
]
extensions.extend(custom_extensions)

myst_enable_extensions = [
    'substitution',
    'deflist',
    'linkify'
]
myst_enable_extensions.extend(custom_myst_extensions)

if 'discourse_prefix' not in html_context and 'discourse' in html_context:
    html_context['discourse_prefix'] = html_context['discourse'] + '/t/'

if slug:
    notfound_urls_prefix = '/' + slug + '/en/latest/'

notfound_context = {
    'title': 'Page not found',
    'body': '<h1>Page not found</h1>\n\n<p>Sorry, but the documentation page that you are looking for was not found.</p>\n<p>Documentation changes over time, and pages are moved around. We try to redirect you to the updated content where possible, but unfortunately, that didn\'t work this time (maybe because the content you were looking for does not exist in this version of the documentation).</p>\n<p>You can try to use the navigation to locate the content you\'re looking for, or search for a similar page.</p>\n',
}

if 'ogp_image' not in locals():
    ogp_image = '_static/ngkore-logo.svg'

############################################################
### General configuration
############################################################

exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '.sphinx',
]
exclude_patterns.extend(custom_excludes)

rst_epilog = '''
.. include:: /reuse/links.txt
'''
if 'custom_rst_epilog' in locals():
    rst_epilog = custom_rst_epilog

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

if 'conf_py_path' not in html_context and 'github_folder' in html_context:
    html_context['conf_py_path'] = html_context['github_folder']

linkcheck_anchors_ignore_for_url = [
    r'https://github\.com/.*',
    "https://matrix.to/*"
]
linkcheck_anchors_ignore_for_url.extend(custom_linkcheck_anchors_ignore_for_url)
linkcheck_ignore = [r'http://.*\.mgmt/']

for tag in custom_tags:
    tags.add(tag)

############################################################
### Styling
############################################################

builder = 'dirhtml'
if '-b' in sys.argv:
    builder = sys.argv[sys.argv.index('-b')+1]

# epub builder fails with templates_path set
if builder in ('dirhtml', 'html'):
    templates_path = ['.sphinx/_templates']

html_theme = 'furo'
html_permalinks_icon = '¶'

if html_title == '':
    html_theme_options = {
        'sidebar_hide_name': True
        }

############################################################
### Additional files
############################################################

html_static_path = ['.sphinx/_static']

html_css_files = [
    'theme.css',
    'typography.css',
    'content.css',
    'layout.css',
    'github_issue_links.css',
    'bottom-logo.css'
]
html_css_files.extend(custom_html_css_files)

html_js_files = []
if 'github_issues' in html_context and html_context['github_issues'] and not disable_feedback_button:
    html_js_files.append('github_issue_links.js')
html_js_files.extend(custom_html_js_files)
