#!/usr/bin/env python3
"""news-image-20261124: write the day's front page to /output/entry.png.

The entry image sits next to this file as entry.png. It is a JPEG of the
front page "THE WORLD TODAY" for Tuesday 24 November 2026, drawn with PIL
by build_image.py from the real stories reported that day. This program
copies it to the output directory byte for byte, so both grading runs
produce identical output. Standard library only, no network.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
SOURCE = os.path.join(HERE, "entry.png")
TARGET = os.path.join(OUT_DIR, "entry.png")

# The competition gate: at most 1 MiB and at most 1024x1024 pixels.
MAX_BYTES = 1048576
MAX_SIDE = 1024


def _jpeg_size(path):
    """Read width and height out of a JPEG header, no dependencies."""
    with open(path, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise ValueError("entry.png is not a JPEG")
        while True:
            marker = fh.read(2)
            if len(marker) < 2 or marker[0] != 0xFF:
                raise ValueError("bad JPEG marker")
            code = marker[1]
            if code in (0xC0, 0xC1, 0xC2):
                fh.read(3)
                raw = fh.read(4)
                height, width = struct.unpack(">HH", raw)
                return width, height
            length = struct.unpack(">H", fh.read(2))[0]
            fh.seek(length - 2, 1)


def main():
    if not os.path.isfile(SOURCE):
        raise SystemExit("entry.png is missing next to main.py")
    with open(SOURCE, "rb") as fh:
        if fh.read(2) != b"\xff\xd8":
            raise SystemExit("entry.png is not a JPEG file")
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SOURCE, TARGET)
    size = os.path.getsize(TARGET)
    if size > MAX_BYTES:
        raise SystemExit("entry.png is %d bytes, over the 1 MiB gate" % size)
    width, height = _jpeg_size(TARGET)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise SystemExit("entry.png is %dx%d, over 1024x1024"
                         % (width, height))
    print("wrote %s: %dx%d, %d bytes" % (TARGET, width, height, size))


if __name__ == "__main__":
    main()
