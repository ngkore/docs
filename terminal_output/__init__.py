"""Sphinx directive for rendering styled terminal output blocks."""

import os

import sphinx.addnodes
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util.docutils import SphinxDirective
from sphinx_utils import add_css


def parse_contents(contents):
    """Split directive content into output blocks and :input: commands."""
    command_output = []
    result = []

    for line in contents:
        if line.startswith(":input: "):
            result.append(command_output)
            result.append([line])
            command_output = []
        else:
            command_output.append(line)

    result.append(command_output)
    return result


class TerminalOutput(SphinxDirective):
    """Render a terminal session with prompt, commands, and output."""

    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {
        "input": directives.unchanged,
        "user": directives.unchanged,
        "host": directives.unchanged,
        "dir": directives.unchanged,
        "scroll": directives.unchanged,
    }

    @staticmethod
    def input_line(prompt_text, command):
        """Build a docutils node for a single prompt + command line."""
        inpline = nodes.container()
        inpline["classes"].append("input")

        prompt_container = nodes.container()
        prompt_container["classes"].append("prompt")
        prompt_container.append(nodes.literal(text=prompt_text))

        inpline.append(prompt_container)
        inp = nodes.literal(text=command)
        inp["classes"].append("command")
        inpline.append(inp)
        return inpline

    def run(self):
        """Parse options and content, return terminal container node."""
        command = self.options.get("input", "")
        user = self.options.get("user", "user")
        host = self.options.get("host", "host")
        working_dir = self.options.get("dir", "~")
        user_symbol = "#" if user == "root" else "$"

        if user and host:
            prompt_text = f"{user}@{host}:{working_dir}{user_symbol} "
        elif user:
            prompt_text = f"{user}:{working_dir}{user_symbol} "
        else:
            prompt_text = f"{working_dir}{user_symbol} "

        out = nodes.container()
        out["classes"].append("terminal")
        out.append(
            sphinx.addnodes.highlightlang(
                lang="text", force=False, linenothreshold=10000
            )
        )
        if "scroll" in self.options:
            out["classes"].append("scroll")

        out.append(self.input_line(prompt_text, command))

        parsed_content = parse_contents(self.content)

        for blob in filter(None, parsed_content):
            if blob[0].startswith(":input: "):
                out.append(self.input_line(prompt_text, blob[0][len(":input: "):]))
            else:
                output = nodes.literal_block(text="\n".join(blob))
                output["classes"].append("terminal-code")
                out.append(output)

        return [out]


def setup(app):
    """Register the terminal directive and its stylesheet."""
    app.add_directive("terminal", TerminalOutput)
    add_css(app, "terminal-output.css", os.path.dirname(__file__))
    return {"version": "0.1", "parallel_read_safe": True,
            "parallel_write_safe": True}
