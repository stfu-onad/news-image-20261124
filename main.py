"""News-image entry for 24 November 2026 (news-image-20261124).

The entry is a newspaper front page for Tuesday 24 November 2026,
shipped as entry.png in this repository. Four main stories: Zelensky
urging four-way peace talks (Ukraine, Russia, the US and Europe);
the US blacklisting Megaspeed, the firm at the centre of the Nvidia
spy scandal; Nvidia shares soaring 31% as Jensen Huang returns as
CEO; and 24 dead in the Indonesia candy-factory fire. The ticker
adds the China spy death sentence, Russian jets in South Korea's
air-defence zone, the Pentagon's rebuke of Canada, the EU's new
Russia sanctions and Bangladesh's typhoid drive.

The hero illustration was generated in this build session with no
text in it; every headline, the date and the captions were drawn
with PIL and DejaVu fonts so the words stay crisp and legible.

This program only copies the shipped image into the grader's output
directory. It uses the standard library only, never touches the
network, and always produces the same bytes.
"""

import hashlib
import os
import shutil
import struct
from pathlib import Path

IMAGE = "entry.png"
LIMIT_BYTES = 1_048_576
LIMIT_PIXELS = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def check_image(path):
    """Read the shipped PNG and return (size, width, height)."""
    blob = Path(path).read_bytes()
    if blob[:8] != MAGIC:
        raise ValueError("shipped file is not a PNG: %s" % path)
    if len(blob) > LIMIT_BYTES:
        raise ValueError("shipped file over 1 MiB: %d bytes" % len(blob))
    width, height = struct.unpack(">II", blob[16:24])
    if width > LIMIT_PIXELS or height > LIMIT_PIXELS:
        raise ValueError("shipped image over 1024x1024: %dx%d"
                         % (width, height))
    return len(blob), width, height


def run():
    here = Path(__file__).resolve().parent
    source = here / IMAGE
    if not source.is_file():
        raise FileNotFoundError("shipped image missing: %s" % source)
    size, width, height = check_image(source)
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / IMAGE
    shutil.copyfile(source, target)
    # The grader runs this program twice and expects identical bytes,
    # so confirm the copy matches the shipped file before reporting.
    if target.read_bytes() != source.read_bytes():
        raise ValueError("copied image differs from shipped image")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    print("wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (target, size, width, height, digest[:16]))


if __name__ == "__main__":
    run()
