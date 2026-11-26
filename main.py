#!/usr/bin/env python3
"""One-Liner Laughs entry for account B (keen-panda-72).

The program writes a single joke line to ``entry.txt`` inside the
output directory. The directory comes from ``MAKEFUN_OUTPUT_DIR`` and
defaults to ``/output`` when the variable is unset or empty.

The house gate requires the file to be UTF-8 text, 1 to 200
characters, not only whitespace, and a single line. This program
enforces the same limits on the line before it writes anything, and
then reads the file back to confirm the bytes on disk are exactly
the line it intended to write. Nothing is read from the working
directory and nothing is written anywhere except ``entry.txt``.

The line: a midnight snack request, a fridge that sighs, orders a
salad and texts the doctor -- the appliances are staging an
intervention.
"""

import os
import sys

ENTRY = (
    "I asked my smart fridge for a midnight snack \u2014 it sighed, "
    "ordered a salad, and texted my doctor. I think my appliances "
    "are staging an intervention."
)

LIMIT = 200


def validate(line):
    """Refuse any line that would fail the house gate.

    Returns the line unchanged when it passes. Exits with an error
    message on the first problem found, so a bad line never reaches
    the output file.
    """
    if not line:
        sys.exit("entry line is empty")
    if line.strip() == "":
        sys.exit("entry line is only whitespace")
    if line != line.strip():
        sys.exit("entry line has leading or trailing whitespace")
    if not line.isprintable():
        sys.exit("entry line contains non-printable or control characters")
    if len(line) > LIMIT:
        sys.exit("entry line is %d chars, over the %d limit" % (len(line), LIMIT))
    return line


def resolve_output_dir():
    """Pick the output directory and create it if needed."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(chosen, exist_ok=True)
    return chosen


def write_entry(directory, line):
    """Write the line to entry.txt and confirm it landed intact."""
    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(target, "rb") as handle:
        on_disk = handle.read()
    if on_disk != line.encode("utf-8"):
        sys.exit("entry.txt on disk differs from the entry line")
    return target


def main():
    line = validate(ENTRY)
    directory = resolve_output_dir()
    target = write_entry(directory, line)
    print("%s -> %s (%d chars)" % (target, line, len(line)))


if __name__ == "__main__":
    main()
