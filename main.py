#!/usr/bin/env python3
"""Two Days of Quiet Dread — one-line PR approval with quiet dread.

Writes a single code-review comment (one line, <=140 chars) to
$MAKEFUN_OUTPUT_DIR/entry.txt. Stdlib only.
"""
import os

ENTRY = (
    "Approved. The alert is actionable, "
    "assuming anyone is still on call when it fires."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(ENTRY + "\n")


if __name__ == "__main__":
    main()
