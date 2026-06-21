"""Sphinx directive for embedding YouTube video links."""

import os

import requests
from bs4 import BeautifulSoup
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.util import logging
from sphinx_utils import add_css

cache = {}
logger = logging.getLogger(__name__)

YOUTUBE_LINK_TEMPLATE = (
    '<p class="youtube_link">'
    '<a href="{url}" target="_blank">'
    '<span title="{title}" class="play_icon">▶</span>'
    '<span title="{title}">Watch on YouTube</span>'
    '</a>'
    '</p>'
)


class YouTubeLink(Directive):
    """Render a styled link to a YouTube video with auto-fetched title."""

    required_arguments = 1
    optional_arguments = 0
    has_content = False
    option_spec = {"title": directives.unchanged}

    def run(self):
        """Build HTML fragment for the YouTube link."""
        url = self.arguments[0]
        title = self._resolve_title(url)
        fragment = YOUTUBE_LINK_TEMPLATE.format(url=url, title=title)
        return [nodes.raw(text=fragment, format="html")]

    def _resolve_title(self, url):
        """Return explicit title, cached title, or fetch from YouTube page."""
        if "title" in self.options:
            return self.options["title"]

        if url in cache:
            return cache[url]

        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            title = soup.title.get_text()
            cache[url] = title
            return title
        except requests.HTTPError as err:
            logger.warning("Failed to fetch YouTube title: %s", err)
            return ""


def setup(app):
    """Register the youtube directive and its stylesheet."""
    app.add_directive("youtube", YouTubeLink)
    add_css(app, "youtube.css", os.path.dirname(__file__))
    return {"version": "0.1", "parallel_read_safe": True,
            "parallel_write_safe": True}
