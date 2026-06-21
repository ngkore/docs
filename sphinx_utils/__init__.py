"""Shared utilities for custom Sphinx extensions."""

from os import path
from sphinx.util.fileutil import copy_asset_file


def _copy_static_file(app, exc, source_dir, filename):
    """Copy a static file from source_dir/_static/ to the build output."""
    if not exc and app.builder.format == "html":
        dest = path.join(app.builder.outdir, "_static", filename)
        src = path.join(source_dir, "_static", filename)
        copy_asset_file(src, dest)


def add_css(app, filename, package_dir):
    """Register a CSS file and copy it to build output on finish."""
    app.connect(
        "build-finished",
        lambda app, exc: _copy_static_file(app, exc, package_dir, filename)
    )
    app.add_css_file(filename)


def add_js(app, filename, package_dir):
    """Register a JS file and copy it to build output on finish."""
    app.connect(
        "build-finished",
        lambda app, exc: _copy_static_file(app, exc, package_dir, filename)
    )
    app.add_js_file(filename)
