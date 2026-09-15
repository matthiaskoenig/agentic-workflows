"""Checks of the documentation site.

The site must build without warnings, every page must be reachable through the
navigation, internal links must resolve, and the markdown must follow the
writing rules of `CLAUDE.md`: no em dash and no hard-wrapped paragraphs.
"""

import re
import subprocess
import sys
import tomllib
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"
CONFIG = ROOT / "zensical.toml"

# markdown files outside `docs/` which follow the same writing rules
EXTRA_MARKDOWN = [ROOT / "CLAUDE.md", ROOT / "README.md"]

EM_DASH = "—"
FENCE = re.compile(r"^(```|~~~)")
BLOCK_START = re.compile(r"^(#|\||!!!|\?\?\?|===|<|---|\*\*\*|___|\[[^\]]+\]:\s)")
LIST_ITEM = re.compile(r"^([-*+]|\d+[.)])\s")
LINK = re.compile(r"\]\(([^)\s]+)\)")


def markdown_files() -> list[Path]:
    """All markdown files that follow the writing rules."""
    files = sorted(DOCS.rglob("*.md")) + sorted((ROOT / "release-notes").glob("*.md"))
    return files + [p for p in EXTRA_MARKDOWN if p.exists()]


def nav_pages(nav: list) -> Iterator[str]:
    """Yield every page path of the (nested) `nav` of `zensical.toml`."""
    for entry in nav:
        for value in entry.values():
            if isinstance(value, str):
                yield value
            else:
                yield from nav_pages(value)


def config_nav() -> list[str]:
    """The page paths of the navigation, in order."""
    with CONFIG.open("rb") as f:
        config = tomllib.load(f)
    return list(nav_pages(config["project"]["nav"]))


def text_lines(path: Path) -> Iterator[tuple[int, str]]:
    """Lines of a markdown file outside code fences and the front matter."""
    lines = path.read_text(encoding="utf-8").split("\n")
    in_fence: str | None = None
    in_front = False
    for number, line in enumerate(lines, start=1):
        stripped = line.strip()
        if number == 1 and stripped == "---":
            in_front = True
            continue
        if in_front:
            if stripped == "---":
                in_front = False
            continue
        if in_fence:
            if stripped.startswith(in_fence):
                in_fence = None
            continue
        match = FENCE.match(stripped)
        if match:
            in_fence = match.group(1)
            continue
        yield number, line


def line_kind(line: str) -> str:
    """Classify a markdown line for the wrapping check."""
    stripped = line.strip()
    if not stripped:
        return "blank"
    if BLOCK_START.match(stripped) or stripped == ">":
        return "block"
    if LIST_ITEM.match(stripped):
        return "list"
    if stripped.startswith(">"):
        return "quote"
    if stripped.startswith(":"):
        return "def"
    return "para"


@pytest.fixture(scope="session")
def build() -> subprocess.CompletedProcess[str]:
    """Build the site once in strict mode."""
    return subprocess.run(
        [sys.executable, "-m", "zensical", "build", "--clean", "--strict"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def test_build_succeeds(build: subprocess.CompletedProcess[str]) -> None:
    """The strict build exits cleanly and writes the index page."""
    assert build.returncode == 0, build.stdout + build.stderr
    assert (SITE / "index.html").is_file()
    assert (SITE / "search.json").is_file()


def test_build_reports_no_issues(build: subprocess.CompletedProcess[str]) -> None:
    """The build log contains no warnings or errors."""
    output = build.stdout + build.stderr
    assert "No issues found" in output, output
    assert not re.search(r"\b(WARNING|ERROR)\b", output), output


def test_every_nav_entry_has_a_page(build: subprocess.CompletedProcess[str]) -> None:
    """Each navigation entry points at a source file and is rendered."""
    assert build.returncode == 0
    for page in config_nav():
        source = DOCS / page
        assert source.is_file(), f"nav entry without source: {page}"
        # `a/index.md` renders to `a/index.html`, `a/b.md` to `a/b/index.html`
        if page.endswith("index.md"):
            rendered = SITE / page.removesuffix("index.md") / "index.html"
        else:
            rendered = SITE / page.removesuffix(".md") / "index.html"
        assert rendered.is_file(), f"nav entry not rendered: {page}"


def test_every_page_is_in_the_nav() -> None:
    """A page that is not in the navigation is unreachable."""
    pages = {str(p.relative_to(DOCS)) for p in DOCS.rglob("*.md")}
    missing = pages - set(config_nav())
    assert not missing, f"pages missing from nav in zensical.toml: {sorted(missing)}"


@pytest.mark.parametrize(
    "path", markdown_files(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_internal_links_resolve(path: Path) -> None:
    """Relative links to markdown files point at existing files."""
    broken = []
    for number, line in text_lines(path):
        for target in LINK.findall(line):
            if target.startswith(("http://", "https://", "mailto:", "#", "/")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part.endswith(".md"):
                continue
            if not (path.parent / file_part).is_file():
                broken.append(f"{path.name}:{number}: {target}")
    assert not broken, "\n".join(broken)


@pytest.mark.parametrize(
    "path", markdown_files(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_no_em_dash(path: Path) -> None:
    """The em dash is never used, see CLAUDE.md."""
    hits = [f"{path.name}:{n}" for n, line in text_lines(path) if EM_DASH in line]
    assert not hits, "em dash in " + ", ".join(hits)


@pytest.mark.parametrize(
    "path", markdown_files(), ids=lambda p: str(p.relative_to(ROOT))
)
def test_no_hard_wrapped_paragraphs(path: Path) -> None:
    """A paragraph, list item or quote is one line; the editor soft-wraps."""
    wrapped = []
    previous = "blank"
    for number, line in text_lines(path):
        kind = line_kind(line)
        if (kind == "para" and previous in {"para", "list", "def"}) or (
            kind == "quote" and previous == "quote"
        ):
            wrapped.append(f"{path.name}:{number}")
        previous = kind
    assert not wrapped, "hard-wrapped lines in " + ", ".join(wrapped)
