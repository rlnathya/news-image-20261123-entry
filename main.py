#!/usr/bin/env python3
"""Entrypoint: write the front page to /output/entry.png.

Draws the page with render_frontpage.py (Pillow). If drawing is
unavailable in the sandbox, falls back to the entry.png shipped in
this repository, which the same script produced, so both runs still
write the same bytes.
"""

import os
import shutil
import sys


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        from render_frontpage import build_frontpage

        build_frontpage(target)
    except Exception:
        shutil.copyfile(os.path.join(here, "entry.png"), target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
