"""Custom RST roles: spellexception, literalref, and none."""

import re
from typing import cast

from docutils import nodes
from sphinx import addnodes
from sphinx.builders import Builder
from sphinx.domains.std import StandardDomain
from sphinx.environment import BuildEnvironment
from sphinx.util.docutils import ReferenceRole
from typing_extensions import override


def spellexception_role(
    name, rawtext, text, lineno, inliner, options=None, content=None
):
    """Wrap text in <spellexception> tags to exclude from spell checking."""
    node = nodes.raw(
        text="<spellexception>" + text + "</spellexception>", format="html"
    )
    return [node], []


def none_role(
    name, rawtext, text, lineno, inliner, options=None, content=None
):
    """Consume role content and produce no output."""
    return [], []


class LiteralrefRole(ReferenceRole):
    """Cross-reference role that renders link text in monospace."""

    def run(self) -> tuple[list[nodes.Node], list[nodes.system_message]]:
        """Create an internal or external reference with monospaced text."""
        node: nodes.reference | addnodes.pending_xref

        if re.match(r"^(https?:\/\/\S+|\S+\.\S{2,3}\/?)\b", self.target):
            self.target = (
                f"https://{self.target}"
                if "://" not in self.target
                else self.target
            )
            node = nodes.reference("", "", internal=False, refuri=self.target)
        else:
            node = addnodes.pending_xref(
                "",
                refdomain="lrd",
                reftype="ref",
                reftarget=self.target,
                refexplicit=True,
                refwarning=True,
            )

        node.append(nodes.literal(text=self.title))
        return [node], []


class LiteralrefDomain(StandardDomain):
    """Custom domain that preserves monospace formatting on resolved refs."""

    name: str = "lrd"

    @override
    def resolve_xref(
        self,
        env: BuildEnvironment,
        fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: addnodes.pending_xref,
        contnode: nodes.Element,
    ) -> nodes.reference | None:
        """Resolve the xref, then replace child nodes with the original literal children."""
        if node.get("refdomain") != "lrd":
            return None

        resolved_node = super().resolve_xref(
            env, fromdocname, builder, typ, target, node, contnode
        )

        if (
            resolved_node
            and hasattr(resolved_node, "children")
            and hasattr(node, "children")
        ):
            resolved_node.children = node.children

        return cast(nodes.reference, resolved_node)


def setup(app):
    """Register custom roles and the literalref domain."""
    app.add_domain(LiteralrefDomain)
    app.add_role("spellexception", spellexception_role)
    app.add_role("literalref", LiteralrefRole())
    app.add_role("none", none_role)
    return {"parallel_read_safe": True,
            "parallel_write_safe": True}
