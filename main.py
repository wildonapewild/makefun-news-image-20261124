#!/usr/bin/env python3
"""THE HEMISPHERE — copy-only carrier.

Reads the finished entry.png sitting next to this file, verifies it is a
1024x1024 PNG, and copies it byte-for-byte to the output location.
Standard library only.
"""
import os
import shutil
import struct
import sys

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def verify_png(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or not head.startswith(PNG_SIGNATURE):
        raise ValueError("not a PNG file: bad signature")
    # IHDR chunk: length(4) type(4) width(4) height(4) ...
    ihdr_type = head[12:16]
    if ihdr_type != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", head[16:24])
    if (width, height) != (1024, 1024):
        raise ValueError(f"unexpected dimensions {width}x{height}, want 1024x1024")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found next to main.py", file=sys.stderr)
        return 1
    width, height = verify_png(src)
    if os.path.isdir("/output"):
        dst = "/output/entry.png"
    else:
        out_dir = os.path.join(here, "output")
        os.makedirs(out_dir, exist_ok=True)
        dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # Second-pass verification: the written copy must be byte-identical
    # to the source and must itself pass the PNG dimension check.
    import hashlib

    def digest(p):
        h = hashlib.sha256()
        with open(p, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    src_hash = digest(src)
    dst_hash = digest(dst)
    if src_hash != dst_hash:
        print("verification failed: output differs from source", file=sys.stderr)
        return 1
    verify_png(dst)
    result = {
        "status": "ok",
        "source": src,
        "destination": dst,
        "dimensions": f"{width}x{height}",
        "bytes": os.path.getsize(dst),
        "sha256": dst_hash,
        "byte_identical": True,
    }
    for key, value in result.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
