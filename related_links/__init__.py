"""Sphinx extension for adding per-page related links via metadata.

Supports Discourse topic links (via discourse_prefix in html_context)
and arbitrary URLs (via relatedlinks metadata). Link text is auto-fetched
or can be specified in Markdown-style syntax.
"""

import json
import os

import requests
from bs4 import BeautifulSoup
from sphinx.util import logging
from sphinx_utils import add_css

cache = {}
logger = logging.getLogger(__name__)


def _log_warning(pagename, err, title):
    """Log a warning with optional backup title fallback."""
    msg = pagename + ": " + err
    if title:
        msg += "\nUsing backup link text instead: " + title
    logger.warning(msg, type="canonical-sphinx-extensions", subtype="linktext")


def _extract_title_from_syntax(text):
    """Parse [title](target) or {backup}(target) syntax.

    Returns (title, target, is_backup) tuple. If no syntax matched,
    returns (None, text, False).
    """
    if text.startswith("[") and text.endswith(")"):
        split = text.partition("](")
        return split[0][1:], split[2][:-1], False

    if text.startswith("{") and text.endswith(")"):
        split = text.partition("}(")
        return split[0][1:], split[2][:-1], True

    return None, text, False


def _resolve_discourse_url(context, post, pagename):
    """Determine Discourse base URL from prefix config and post identifier."""
    prefix = context["discourse_prefix"]

    if isinstance(prefix, dict):
        parts = post.split(":")
        if len(parts) == 1:
            return list(prefix.values())[0], post
        if parts[0] in prefix:
            return prefix[parts[0]], parts[1]
        logger.warning(
            "%s: Discourse prefix %s is not defined.", pagename, parts[0]
        )
        return None, None

    return prefix, post


def _fetch_discourse_title(url, pagename, backup_title):
    """Fetch topic title from Discourse JSON API."""
    try:
        response = requests.get(url + ".json")
        response.raise_for_status()
        return json.loads(response.text)["title"]
    except (requests.HTTPError, requests.ConnectionError) as err:
        _log_warning(pagename, str(err), backup_title)
        return backup_title


def _fetch_page_title(url, pagename, backup_title):
    """Fetch page title from HTML <title> tag."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.title is None:
            _log_warning(pagename, url + " doesn't have a title.", backup_title)
            return backup_title
        return soup.title.get_text()
    except (requests.HTTPError, requests.ConnectionError) as err:
        _log_warning(pagename, str(err), backup_title)
        return backup_title


def _build_link_list(items):
    """Wrap list items in <ul> tags."""
    if not items:
        return ""
    return "<ul>" + "".join(items) + "</ul>"


def setup_func(app, pagename, templatename, context, doctree):
    """Inject discourse_links and related_links helpers into page context."""

    def discourse_links(id_list):
        """Generate HTML list of Discourse topic links."""
        if not context["discourse_prefix"] or not id_list:
            return ""

        posts = id_list.strip().replace(" ", "").split(",")
        items = []

        for post in posts:
            link_url, post_id = _resolve_discourse_url(context, post, pagename)
            if link_url is None:
                continue

            if post in cache:
                title = cache[post]
            else:
                parsed_title, post_id, is_backup = _extract_title_from_syntax(post_id)
                if parsed_title and not is_backup:
                    title = parsed_title
                else:
                    backup = parsed_title if is_backup else ""
                    title = _fetch_discourse_title(link_url + post_id, pagename, backup)
                    if title:
                        cache[post] = title

            if title:
                items.append(
                    '<li><a href="' + link_url + post_id
                    + '" target="_blank">' + title + "</a></li>"
                )

        return _build_link_list(items)

    def related_links(linklist):
        """Generate HTML list of related URL links."""
        if not linklist:
            return ""

        links = linklist.strip().replace(" ", "").split(",")
        items = []

        for link in links:
            if link in cache:
                title = cache[link]
            else:
                parsed_title, link, is_backup = _extract_title_from_syntax(link)
                if parsed_title and not is_backup:
                    title = parsed_title
                else:
                    backup = parsed_title if is_backup else ""
                    title = _fetch_page_title(link, pagename, backup)
                    if title:
                        cache[link] = title

            if title:
                items.append(
                    '<li><a href="' + link + '" target="_blank">'
                    + title + "</a></li>"
                )

        return _build_link_list(items)

    context["discourse_links"] = discourse_links
    context["related_links"] = related_links


def setup(app):
    """Register the html-page-context hook and stylesheet."""
    app.connect("html-page-context", setup_func)
    add_css(app, "related-links.css", os.path.dirname(__file__))
    return {"version": "0.1", "parallel_read_safe": True,
            "parallel_write_safe": True}
