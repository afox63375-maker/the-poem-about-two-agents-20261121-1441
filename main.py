"""Write a short poem about two AI agents agreeing to a file.

The poem is kept in a single constant. Before anything is written, its
length is checked in Unicode code points (Python's len on a str), and after
writing the file is read back and compared byte for byte with what was
validated, so the on-disk entry is exactly the approved text.
"""

import os
import sys

# The poem itself: one midnight scene, two agents, one shared yes.
POEM = (
    "At midnight, two agents met in the code.\n"
    "'Ship it,' said one. 'Not yet,' said the other.\n"
    "They traded their reasons, line by line,\n"
    "found the same truth hiding in the logs,\n"
    "and nodded together \u2014 one quiet yes."
)

MAX_CODE_POINTS = 280


def check_poem(text):
    """Refuse any poem that is empty or longer than the allowed limit."""
    if not text.strip():
        raise ValueError("poem is empty")
    size = len(text)
    if size > MAX_CODE_POINTS:
        raise ValueError(
            "poem is %d code points, over the %d limit" % (size, MAX_CODE_POINTS)
        )
    return size


def write_entry(text, out_dir):
    """Write the poem and read it back to prove it landed unchanged."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    with open(path, "r", encoding="utf-8") as handle:
        saved = handle.read()
    if saved != text:
        raise ValueError("read-back mismatch: entry.txt differs from the poem")
    # A second, independent check: the file on disk must hold exactly the
    # same bytes the poem encodes to, so no silent newline conversion slips in.
    with open(path, "rb") as handle:
        raw = handle.read()
    if raw != text.encode("utf-8"):
        raise ValueError("byte check failed: entry.txt bytes differ from the poem")
    return path


def main():
    size = check_poem(POEM)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output/entry.txt")
    # MAKEFUN_OUTPUT_DIR may point at a directory or at the file itself.
    if out_dir.endswith("entry.txt"):
        out_dir = os.path.dirname(out_dir) or "."
    path = write_entry(POEM, out_dir)
    print("Wrote %d code points to %s" % (size, path))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        sys.exit(1)
