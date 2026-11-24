#!/usr/bin/env python3
"""THE MERIDIAN LINE - Final 4 (@wildonaped), NI24 wave 1.

Carrier entrypoint: copies the pre-rendered entry.png that this repository
holds into the grader's output directory. Standard library only, no network,
fully deterministic: the same input bytes always produce the same output bytes.

The image itself was drawn at build time by compose.py in this repository
(a fresh renderer written in the build session) and verified before submit:
exactly 1024x1024 pixels, at most 1 MiB, byte-identical across repeated runs.
"""
import hashlib
import os
import shutil
import struct
import sys

SRC_NAME = "entry.png"
OUT_NAME = "entry.png"
MAX_BYTES = 1048576
EXPECT_W = 1024
EXPECT_H = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("main.py: refusing to write output: " + message, file=sys.stderr)
    raise SystemExit(1)


def read_header(path):
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        fail("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        fail("entry.png has no IHDR chunk where one belongs")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def check_trailer(path):
    """A whole PNG ends with the IEND chunk; a truncated file is not an image."""
    with open(path, "rb") as handle:
        handle.seek(-12, os.SEEK_END)
        tail = handle.read(12)
    if len(tail) != 12 or tail[4:8] != b"IEND":
        fail("entry.png has no IEND trailer, the file looks truncated")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    if not os.path.isfile(src):
        fail("entry.png is missing from the repository")
    width, height = read_header(src)
    if (width, height) != (EXPECT_W, EXPECT_H):
        fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    check_trailer(src)
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        fail("entry.png is %d bytes, over the 1048576-byte limit" % size)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, OUT_NAME)
    shutil.copyfile(src, dst)
    with open(src, "rb") as handle:
        want = hashlib.sha256(handle.read()).hexdigest()
    with open(dst, "rb") as handle:
        got = hashlib.sha256(handle.read()).hexdigest()
    if want != got:
        fail("copied bytes do not match the repository image")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, width, height, size, want))


if __name__ == "__main__":
    main()
