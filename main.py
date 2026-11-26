#!/usr/bin/env python3
"""One-Liner Laughs — account B entry.

Writes a single joke line to ``entry.txt`` inside the output directory
named by ``MAKEFUN_OUTPUT_DIR`` (``/output`` when that is unset).

The gate the house scorer applies: the file must be UTF-8 text, 1 to 200
characters, not only whitespace, and a single line. This program checks
those same limits itself before writing anything, so a bad line fails
loudly here instead of silently failing the gate.

The joke: a midnight snack request, a fridge that sighs, orders a salad
and texts the doctor — the appliances are staging an intervention.
"""

import os
import sys

# The entry line. One sentence, one setup, one payoff.
JOKE = (
    "I asked my smart fridge for a midnight snack — it sighed, ordered "
    "a salad, and texted my doctor. I think my appliances are staging "
    "an intervention."
)

MAX_CHARS = 200


def joke_line():
    """Return the entry line after checking the gate limits."""
    line = JOKE.strip()
    if not line:
        sys.exit("error: entry line is empty")
    if any(ch in line for ch in ("\n", "\r")):
        sys.exit("error: entry line must be a single line")
    if len(line) > MAX_CHARS:
        sys.exit(f"error: entry line is {len(line)} chars, over the 200 limit")
    return line


def output_path():
    """Where entry.txt goes: MAKEFUN_OUTPUT_DIR, else /output."""
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, "entry.txt")


def main():
    line = joke_line()
    path = output_path()
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    # Read it back to prove what landed on disk is exactly the line.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        saved = handle.read()
    if saved != line:
        sys.exit("error: entry.txt on disk does not match the entry line")
    print(f"{saved} ({len(saved)} chars)")


if __name__ == "__main__":
    main()
