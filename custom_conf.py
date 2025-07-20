import datetime

# Custom configuration for the Sphinx documentation builder.
# All configuration specific to your project should be done in this file.
#
# The file is included in the common conf.py configuration file.
# You can modify any of the settings below or add any configuration that
# is not covered by the common conf.py file.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
#
# If you're not familiar with Sphinx and don't want to use advanced
# features, it is sufficient to update the settings in the "Project
# information" section.

############################################################
### Project information
############################################################

# Product name
project = 'NgKore'
author = 'Ngkore'

# The title you want to display for the documentation in the sidebar.
# You might want to include a version number here.
# To not display any title, set this option to an empty string.
html_title = project + ' Docs'

# Copyright configuration for NgKore
copyright = '2023 NgKore Community. All rights reserved.'

## Open Graph configuration - defines what is displayed as a link preview
## when linking to the documentation from another website (see https://ogp.me/)
# The URL where the documentation will be hosted (leave empty if you
# don't know yet)
ogp_site_url = "https://docs.ngkore.org"
# The documentation website name (usually the same as the product name)
ogp_site_name = project
# The URL of an image or logo that is used in the preview
ogp_image = ".sphinx/_static/tag.png"

# Update with the local path to the favicon for your product
# (default is the circle of friends)
html_favicon = '.sphinx/_static/favicon.ico'

# (Some settings must be part of the html_context dictionary, while others
#  are on root level. Don't move the settings.)
html_context = {

    # Change to the link to the website of your product (without "https://")
    # If there is no product website, edit the header template to remove the
    # link (see the readme for instructions).
    'product_page': 'github.com/ngkore',

    # Add your product tag (the orange part of your logo, will be used in the
    # header) to ".sphinx/_static" and change the path here (start with "_static")
    # (default is the circle of friends)
    'product_tag': '_static/tag.png',

    # Change to the discourse instance you want to be able to link to
    # using the :discourse: metadata at the top of a file
    # (use an empty value if you don't want to link)
    # 'discourse': 'https://ngkore.org',

    # Change to the GitHub URL for your project
    'github_url': 'https://github.com/ngkore/docs',

    # Change to the branch for this version of the documentation
    'github_version': 'main',

    # Change to the folder that contains the documentation
    # (usually "/" or "/docs/")
    'github_folder': '/',

    # Change to an empty value if your GitHub repo doesn't have issues enabled.
    # This will disable the feedback button and the issue link in the footer.
    # 'github_issues': 'enabled',

    # Controls the existence of Previous / Next buttons at the bottom of pages
    # Valid options: none, prev, next, both
    # 'sequential_nav': "both"
}

# slug (for example, "lxd") here.
slug = ""

# Base URL and environment configuration
import os

# Detect if we're building for GitHub Pages
is_production = os.environ.get('GITHUB_ACTIONS', False) or os.environ.get('READTHEDOCS', False)

if is_production:
    html_baseurl = '/'  # For custom domain GitHub Pages
    # Ensure absolute URLs for production
    html_theme_options_extra = {}
else:
    html_baseurl = '/'
    html_theme_options_extra = {}

############################################################
### Redirects
############################################################

# Set up redirects (https://documatt.gitlab.io/sphinx-reredirects/usage.html)
# For example: 'explanation/old-name.html': '../how-to/prettify.html',

redirects = {
    'ebpf/introduction-to-ebpf/': '../understanding-ebpf-in-kernel/',
    'ebpf/ebpf-based-l4-load-balancer/': '../building-ebpf-based-l4-load-balancer/',
    'ebpf/ebpf-in-ssd/': '../data-processing-with-ebpf-in-ssd/',
    'ebpf/ebpf-in-gpu-acceleration/': '../ebpf-for-gpu-acceleration/',
}

############################################################
### Link checker exceptions
############################################################

# Links to ignore when checking links

linkcheck_ignore = ['http://127.0.0.1:8000']

# Pages on which to ignore anchors
# (This list will be appended to linkcheck_anchors_ignore_for_url)

custom_linkcheck_anchors_ignore_for_url = []

############################################################
### Additions to default configuration
############################################################

## The following settings are appended to the default configuration.
## Use them to extend the default functionality.

# Add extensions
custom_extensions = []

# Add MyST extensions
custom_myst_extensions = []

# Add files or directories that should be excluded from processing.
custom_excludes = ['venv/**']

# Add CSS files (located in .sphinx/_static/)
custom_html_css_files = ['hide-footer-text.css', 'footer-icons.css', 'ngkore-theme.css']

# Add JavaScript files (located in .sphinx/_static/)
custom_html_js_files = ['custom-theme-toggle.js']

# Ensure proper static files configuration for GitHub Pages
if is_production:
    # Additional production-specific static file handling
    html_extra_path = []  # Add any extra paths if needed
    
    # Ensure proper link resolution for GitHub Pages
    html_use_index = True
    html_file_suffix = ''
    html_link_suffix = '/'
    
    # Static files already configured in main conf.py

## The following settings override the default configuration.

# Specify a reST string that is included at the end of each file.
# If commented out, use the default (which pulls the reuse/links.txt
# file into each reST file).
# custom_rst_epilog = ''

# By default, the documentation includes a feedback button at the top.
# You can disable it by setting the following configuration to True.
disable_feedback_button = False

# Add tags that you want to use for conditional inclusion of text
# (https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#tags)
custom_tags = []

############################################################
### Additional configuration
############################################################

myst_heading_anchors = 3

# Furo theme configuration
html_theme_options = {
    "source_repository": "https://github.com/ngkore/docs",
    "source_branch": "main",
    "source_directory": "",
    "footer_icons": [
        {
            "name": "Email",
            "url": "mailto:contact@ngkore.org",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "LinkedIn",
            "url": "https://www.linkedin.com/company/ngkore/",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "X (Twitter)",
            "url": "https://x.com/kore_ng",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.901 1.153h3.68l-8.04 9.19L24 22.846h-7.406l-5.8-7.584-6.638 7.584H.474l8.6-9.83L0 1.154h7.594l5.243 6.932ZM17.61 20.644h2.039L6.486 3.24H4.298Z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/ngkore",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "YouTube",
            "url": "https://www.youtube.com/@NgKore",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
            """,
            "class": "",
        },
    ],
}

# Hide Sphinx attribution and last updated information
html_show_sphinx = False
html_last_updated_fmt = None

# Override any existing theme options and merge with footer icons
if 'html_theme_options' not in locals():
    html_theme_options = {}

html_theme_options.update({
    # Remove source repository to disable edit button
    # "source_repository": "https://github.com/ngkore/docs",
    # "source_branch": "main", 
    # "source_directory": "",
})

# Merge production-specific theme options
html_theme_options.update(html_theme_options_extra)

## Add any configuration that is not covered by the common conf.py file.
