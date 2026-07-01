import glob
import os

############################################################
### Project information
############################################################

project = 'NgKore'
author = 'NgKore Foundation'

html_title = project + ' Documentation'

copyright = '2023-2025 NgKore Foundation. All rights reserved.'

# Open Graph link preview configuration
ogp_site_url = "https://docs.ngkorefoundation.org"
ogp_site_name = project
ogp_image = ".sphinx/_static/tag.png"

ogp_description = 'NgKore Foundation is an open-source community driving innovation across Quantum Safe Network, PQC, eBPF, 5G Advanced, 6G, O-RAN, NTN, AI/ML, Blockchain, and Quantum Simulations.'

html_meta = {
    'description': 'NgKore Foundation is an open-source community driving innovation across Quantum Safe Network, PQC, eBPF, 5G Advanced, 6G, O-RAN, NTN, AI/ML, Blockchain, and Quantum Simulations.',
    'keywords': '5G Core, PQC, post-quantum cryptography, eBPF, XDP, O-RAN, network security, AI/ML, kernel bypass, UPF, TLS, IPSec, QUIC, NTN, satellite networks, xFAPI, SMO, RIC, DPDK, AF_XDP, SRIOV, Quantum, OQS, Kubernetes, HEXAeBPF, 6G, Blockchain, Quantum Simulations, Telecom',
    'author': 'NgKore Foundation',
    'robots': 'index, follow',
    'og:type': 'website',
    'og:description': 'NgKore Foundation is an open-source community driving innovation across Quantum Safe Network, PQC, eBPF, 5G Advanced, 6G, O-RAN, NTN, AI/ML, Blockchain, and Quantum Simulations.',
    'twitter:card': 'summary_large_image',
    'twitter:site': '@ngkore_org',
}

html_favicon = '.sphinx/_static/favicon.ico'

html_context = {
    'product_page': 'github.com/ngkore',
    'product_tag': '_static/tag.png',
    'github_url': 'https://github.com/ngkore/docs',
    'github_version': 'main',
    'github_folder': '/',
}

slug = ""

is_production = os.environ.get(
    'GITHUB_ACTIONS', False) or os.environ.get('READTHEDOCS', False)

############################################################
### Redirects
############################################################

redirects = {
    'ebpf/introduction-to-ebpf/': '../understanding-ebpf-in-kernel/',
    'ebpf/ebpf-based-l4-load-balancer/': '../building-ebpf-based-l4-load-balancer/',
    'ebpf/ebpf-in-ssd/': '../data-processing-with-ebpf-in-ssd/',
    'ebpf/ebpf-in-gpu-acceleration/': '../ebpf-for-gpu-acceleration/',
    '5g-core/standards/': '../open-source-comparison/',
    '5g-core/standards/oai-free5gc-open5gs-magma-5g-core-standards-for-amf/': '../../open-source-comparison/oai-free5gc-open5gs-magma-5g-core-standards-for-amf/',
    '5g-core/standards/oai-free5gc-open5gs-and-magma-5g-core-standards-for-smf/': '../../open-source-comparison/oai-free5gc-open5gs-and-magma-5g-core-standards-for-smf/',
    '5g-core/standards/oai-free5gc-open-5gs-5g-core-standards-for-upf/': '../../open-source-comparison/oai-free5gc-open-5gs-5g-core-standards-for-upf/',
    '5g-core/standards/5g-core-nf-apis-across-releases/': '../../open-source-comparison/5g-core-nf-apis-across-releases/',
    '5g-core/standards/ngap-procedures-comparison/': '../../open-source-comparison/ngap-procedures-comparison/',
    '5g-core/os-5gc-compare/': 'open-source-comparison/os-5gc-compare/',
}

############################################################
### Link checker exceptions
############################################################

linkcheck_ignore = ['http://127.0.0.1:8000']

custom_linkcheck_anchors_ignore_for_url = []

############################################################
### Additions to default configuration
############################################################

custom_extensions = ['sphinx.ext.todo', 'sphinx_sitemap']

custom_myst_extensions = []

custom_excludes = ['venv/**', 'CLAUDE.md', 'README.md']

custom_html_css_files = []

custom_html_js_files = ['custom-theme-toggle.js', 'bottom-logo.js']

if is_production:
    html_use_index = True
    html_file_suffix = ''
    html_link_suffix = '/'

disable_feedback_button = False

custom_tags = []

############################################################
### Additional configuration
############################################################

myst_heading_anchors = 3

html_use_opensearch = 'https://docs.ngkorefoundation.org'
html_baseurl = 'https://docs.ngkorefoundation.org/'

sitemap_url_scheme = "{link}"
sitemap_locales = ['en']
sitemap_excludes = [
    'search/',
    'genindex/',
    'opensearch/',
    '404/',
    'repository-conventions/',
    'how-to-contribute/',
]

html_extra_path = []
if os.path.exists('robots.txt'):
    html_extra_path.append('robots.txt')

if os.path.isdir('images') and 'images' not in html_extra_path:
    html_extra_path.append('images')

# Include PDF parent directories to preserve directory structure in build output
pdf_files = [
    p for p in glob.glob('**/*.pdf', recursive=True)
    if not p.startswith('_build/') and not p.startswith('.sphinx/')
]
pdf_dirs = sorted({os.path.dirname(p) or '.' for p in pdf_files})
html_extra_path.extend(pdf_dirs)

html_theme_options = {
    "source_repository": "https://github.com/ngkore/docs",
    "source_branch": "main",
    "source_directory": "",
    "footer_icons": [
        {
            "name": "Website",
            "url": "https://ngkorefoundation.org/",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "Email",
            "url": "mailto:contact@ngkorefoundation.org",
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
            "name": "Matrix",
            "url": "https://matrix.to/#/#ngkore:matrix.org",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M.632.55v22.9H2.28V24H0V0h2.28v.55zm7.043 7.26v1.157h.033c.309-.443.683-.784 1.117-1.024.433-.245.936-.365 1.5-.365.54 0 1.033.107 1.481.314.448.208.785.582 1.02 1.108.254-.374.6-.706 1.034-.992.434-.287.95-.43 1.546-.43.453 0 .872.056 1.26.167.388.11.716.286.993.53.276.245.489.559.646.951.152.392.23.863.23 1.417v5.728h-2.349V11.52c0-.286-.01-.559-.032-.812a1.755 1.755 0 0 0-.18-.66 1.106 1.106 0 0 0-.438-.448c-.194-.11-.457-.166-.785-.166-.332 0-.6.064-.803.189a1.38 1.38 0 0 0-.48.499 1.946 1.946 0 0 0-.231.696 5.56 5.56 0 0 0-.06.785v4.768h-2.35v-4.8c0-.254-.004-.503-.018-.752a2.074 2.074 0 0 0-.143-.688 1.052 1.052 0 0 0-.415-.503c-.194-.125-.476-.19-.854-.19-.111 0-.259.024-.439.074-.18.051-.36.143-.53.282-.171.138-.319.337-.439.595-.12.259-.18.6-.18 1.02v4.966H5.46V7.81zm15.693 15.64V.55H21.72V0H24v24h-2.28v-.55z"/>
                </svg>
            """,
            "class": "",
        },
        {
            "name": "X (Twitter)",
            "url": "https://x.com/ngkore_org",
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
            "url": "https://www.youtube.com/@ngkore",
            "html": """
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
                </svg>
            """,
            "class": "",
        },
    ],
}

html_show_sphinx = False
html_last_updated_fmt = None
