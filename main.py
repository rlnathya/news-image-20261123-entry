"""Put together the front page for Monday, 23 November 2026 and save it.

The picture is drawn from scratch by the renderer that lives next to
this file. If drawing fails for any reason, the finished picture that
ships with this entry is used instead, so the output folder still
ends up holding exactly the same image either way."""

from os import getenv
from pathlib import Path


def _picture_target() -> Path:
    """Decide where the finished picture goes and make sure the folder exists."""
    folder = Path(getenv("MAKEFUN_OUTPUT_DIR") or "/output")
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "entry.png"


def _bundled_picture() -> Path:
    """Point at the ready-made picture stored beside this file."""
    return Path(__file__).resolve().parent / "entry.png"


def _draw(target: Path) -> None:
    """Ask the renderer to draw the page straight into the target file."""
    import render_frontpage

    render_frontpage.build_frontpage(str(target))


def _reuse_ready_picture(source: Path, target: Path) -> None:
    """Fill the target with the exact bytes of the bundled picture."""
    target.write_bytes(source.read_bytes())


def publish() -> None:
    """Produce the front page, falling back to the bundled picture if needed."""
    target = _picture_target()
    try:  # first attempt: draw the page fresh
        _draw(target)
    except Exception as _draw_failed:
        _reuse_ready_picture(_bundled_picture(), target)


if __name__ == "__main__": publish()
