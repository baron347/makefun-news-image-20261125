#!/usr/bin/env python3
"""Entry point for make.fun news-image-20261125.

Copies the pre-drawn entry image (entry.png, built by build_image.py)
to the harness output directory as entry.png. Deterministic: the same
bytes are written on every run. Standard library only, no network.
"""

import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
