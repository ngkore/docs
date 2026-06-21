# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NgKore Foundation documentation site — Sphinx-based, Markdown-first (MyST parser), Furo theme. Covers PQC, 5G, O-RAN, eBPF, NTN, AI/ML, security, and kernel bypass. Deployed to GitHub Pages via CI.

## Build Commands

```bash
make install          # Create venv at .sphinx/venv, install deps from .sphinx/requirements.txt
make run              # Auto-rebuild + live-reload dev server at localhost:8000
make html             # One-shot build (warnings go to .sphinx/warnings.txt)
make serve            # Serve pre-built output at localhost:8000
make clean-doc        # Remove _build only
make clean            # Remove _build + .sphinx/venv
make spelling         # Spell check (requires pyspelling)
make linkcheck        # Validate external links
make html-github      # Production build (sets GITHUB_ACTIONS=true, creates .nojekyll + index.html copies)
```

All make targets activate the venv at `.sphinx/venv/bin/activate` automatically.

## Architecture

- **conf.py** — Base Sphinx config. Do not edit; put customizations in **custom_conf.py**.
- **custom_conf.py** — Project-specific settings: redirects, SEO meta, theme options, custom extensions, extra CSS/JS.
- **sphinx_utils/** — Shared utilities for custom extensions (static asset registration).
- **Custom Sphinx extensions** (each is a Python package with `__init__.py`):
  - `custom_rst_roles/` — `:spellexception:`, `:literalref:`, `:none:` roles
  - `youtube_links/` — YouTube embed directive
  - `related_links/` — Related links directive
  - `terminal_output/` — Terminal output formatting
- **Content sections** — Each top-level dir (`pqc/`, `5g-core/`, `oran/`, `ebpf/`, `ai-ml/`, `security/`, `kernel-bypass/`, `ntn/`, `tutorials/`) has its own `index.md` with `toctree` and an `images/` subdir.
- **Reusable includes** — `reuse/links.txt` is pulled into every RST file via `rst_epilog`.
- **Static assets** — `.sphinx/_static/` (CSS, JS, logos), `.sphinx/_templates/`.

### CSS Architecture

CSS is split by concern. All files loaded via `html_css_files` in `conf.py`:

| File                     | Responsibility                                                                     |
| ------------------------ | ---------------------------------------------------------------------------------- |
| `theme.css`              | Variables (fonts, colors, light/dark mode), NgKore component theming, footer icons |
| `typography.css`         | Fonts, headings, paragraphs, lists, links, blockquotes                             |
| `content.css`            | Tables, code blocks, admonitions, images, cards, tabs                              |
| `layout.css`             | Sidebar, TOC, content width, responsive overrides, footer visibility               |
| `github_issue_links.css` | Feedback button styling                                                            |
| `bottom-logo.css`        | Bottom-right logo positioning                                                      |

Extensions (`youtube_links`, `related_links`, `terminal_output`) bundle their own CSS in their `_static/` dirs.

## Content Conventions

- **File naming**: lowercase, dash-separated, no filler words. Title "The Future of Quantum Security" → `future-of-quantum-security.md`.
- **Metadata header** on every doc:

  ```markdown
  # Document Title

  **Author:** [Name](https://linkedin.com/in/username/)
  **Published:** Month Day, Year
  ```

- **Header hierarchy**: H1 once (title), then H2→H3→H4 sequentially. Never skip levels — Sphinx warns.
- **Code blocks**: use `console` for terminal output with commands, `bash` for scripts only, `groovy` for Gradle (not `gradle`), `diff` for patches.
- **Images**: store in section's `images/` dir, use relative paths, descriptive lowercase-dash names.
- **Repo links**: use note blocks at top of doc for related repositories.
- **New pages**: add to parent `index.md` toctree.

## Git Conventions

- All commits require DCO sign-off: `git commit -s -m "message"`
- Branch naming: `topic/your-topic-name`
- Commit messages: imperative mood, under 72 chars subject

## CI

GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) builds on push/PR to `main`, deploys to GitHub Pages. Uses `sphinx-build -c . -b dirhtml . _build/html` with `--keep-going`. Build warnings are logged but don't fail the build.

## Dependencies

Two requirements files:

- `requirements.txt` (root) — used by CI pip install
- `.sphinx/requirements.txt` — used by `make install` (includes `sphinx-autobuild` for local dev)
