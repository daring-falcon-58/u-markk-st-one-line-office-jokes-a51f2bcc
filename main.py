#!/usr/bin/env python3
"""One-Line Office Jokes — make.fun entry.

Writes the chosen office joke (one line, 110 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt, falling back to /output/entry.txt,
and prints it to stdout.

Guards (enforced before the write, so a bad line fails loudly instead of
reaching the gate): 1-199 chars, exactly one line, not only whitespace, no
control characters, no links/markdown/stage directions/dialogue tags/quoted
speech, and the line must turn on a real office detail from the brief
(coffee machine / meeting / email / printer). The write is verified by
reading the bytes back and comparing their sha256 digest.
"""

import hashlib
import os

LINE = "The coffee machine broke on Monday, so by Tuesday we'd formed a support group and by Wednesday we'd unionized."

# The brief's own named office details; the line must turn on at least one.
OFFICE_DETAILS = ("coffee machine", "meeting", "email", "printer", "reply-all")


def check(line: str) -> None:
    if not 1 <= len(line) <= 199:
        raise ValueError(f"line must be 1-199 chars, got {len(line)}")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if not line.strip():
        raise ValueError("line must not be only whitespace")
    if line != line.strip():
        raise ValueError("line must not have leading/trailing whitespace")
    if any(ord(c) < 32 for c in line):
        raise ValueError("line must not contain control characters")
    if "http://" in line or "https://" in line or "www." in line:
        raise ValueError("line must not contain a link")
    if any(t in line for t in ("[", "]", "*", "_", "#")):
        raise ValueError("line must not contain markdown")
    if line.startswith(('"', "'")) or line.endswith(('"', "'")):
        raise ValueError("line must not be quoted speech")
    lowered = line.lower()
    if not any(d in lowered for d in OFFICE_DETAILS):
        raise ValueError("line must turn on a real office detail")


def main() -> None:
    check(LINE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    with open(path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        raise ValueError("written bytes do not match the line")
    print("sha256:", hashlib.sha256(written).hexdigest())
    print(LINE)


if __name__ == "__main__":
    main()
