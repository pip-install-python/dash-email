"""Markdown-driven documentation engine.

Globs docs/**/*.md at import time, parses each file's frontmatter and body
with markdown2dash + custom directives, and registers a Dash page per file.
Examples referenced by `.. exec::` are isolated modules exposing a
module-level `component`; `.. source::` shows their source code.
"""
import logging
import re
from pathlib import Path
from typing import List, Optional

import dash
import dash_mantine_components as dmc
import frontmatter
from dash_improve_my_llms import register_page_metadata
from markdown2dash import Admonition, BlockExec, Divider, Image, create_parser
from pydantic import BaseModel

from lib.ad_client import inject_ad_into_aside
from lib.constants import OG_IMAGE_URL, PAGE_TITLE_PREFIX, NAME_CONTENT_MAP
from lib.directives.kwargs import Kwargs
from lib.directives.llms_copy import LlmsCopy
from lib.directives.source import SC
from lib.directives.toc import TOC

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

directory = "docs"

files = Path(directory).glob("**/*.md")


class Meta(BaseModel):
    name: str
    description: str
    endpoint: str
    package: str = "dash_email"
    category: Optional[str] = None
    icon: Optional[str] = None


_SOURCE_DIRECTIVE = re.compile(r'^\.\. source::(.+?)$', re.MULTILINE)
_LANG_MAP = {
    'py': 'python',
    'js': 'javascript', 'jsx': 'jsx',
    'css': 'css',
    'html': 'html',
    'json': 'json',
    'md': 'markdown', 'txt': 'text',
    'sh': 'bash', 'bash': 'bash',
}


def _expand_source_directives(markdown_content: str) -> str:
    """Inline `.. source::path` directives with the referenced file content
    so /<page>/llms.txt is self-contained."""
    def replace(match: re.Match) -> str:
        file_path = match.group(1).strip()
        try:
            full = Path(file_path)
            content = full.read_text()
            ext = full.suffix.lstrip('.').lower()
            lang = _LANG_MAP.get(ext, ext or 'text')
            tail = '' if content.endswith('\n') else '\n'
            return f'\n```{lang}\n# File: {file_path}\n\n{content}{tail}```\n'
        except FileNotFoundError:
            return f'\n<!-- Error: File not found: {file_path} -->\n'
        except Exception as exc:
            return f'\n<!-- Error reading {file_path}: {exc} -->\n'

    return _SOURCE_DIRECTIVE.sub(replace, markdown_content)


def _build_llms_doc(name: str, description: str, expanded_markdown: str, path: str) -> str:
    """Wrap the expanded markdown with the heading/description preamble that
    /llms.txt readers expect."""
    parts: List[str] = [f"# {name}\n"]
    if description:
        parts.append(f"> {description}\n")
    parts.append("---\n")
    parts.append(expanded_markdown.rstrip() + "\n")
    parts.append("\n---\n")
    parts.append(f"*Source: {path}*\n")
    return "\n".join(parts)


directives = [Admonition(), BlockExec(), Divider(), Image(), Kwargs(), LlmsCopy(), SC(), TOC()]
parse = create_parser(directives)

for file in files:
    logger.info("Loading %s..", file)
    metadata, content = frontmatter.parse(file.read_text())
    metadata = Meta(**metadata)

    # Store raw markdown content for the LLM copy button.
    NAME_CONTENT_MAP[metadata.name] = content

    layout = parse(content)

    section = [
        dmc.Title(metadata.name, order=2, className="m2d-heading"),
        dmc.Text(metadata.description, className="m2d-paragraph"),
    ]
    layout = section + layout

    # 2plot.dev ad network: append the ad slot below the TOC links inside
    # the page's aside (pages without `.. toc::` simply get no ad).
    inject_ad_into_aside(layout, metadata.endpoint)

    # `image_url` is absolute and is what stops Dash emitting `og:image=""` on
    # every documentation page. Dash builds og:image/twitter:image from this
    # call (dash/_pages.py); given nothing it INFERS one from the assets folder
    # and, finding no candidate, ships the tag empty — which scrapers read as a
    # declared image and render as a blank card. One URL for every page is
    # correct here: these are documentation pages of one library, not articles
    # with their own artwork.
    dash.register_page(
        metadata.name,
        metadata.endpoint,
        name=metadata.name,
        title=PAGE_TITLE_PREFIX + metadata.name,
        description=metadata.description,
        image_url=OG_IMAGE_URL,
        layout=layout,
        category=metadata.category,
        icon=metadata.icon,
    )

    # Serve the directive-expanded prose at /<page>/llms.txt.
    expanded = _expand_source_directives(content)
    register_page_metadata(
        path=metadata.endpoint,
        name=metadata.name,
        description=metadata.description,
        llms_doc=_build_llms_doc(metadata.name, metadata.description, expanded, metadata.endpoint),
    )
