#!/usr/bin/env python3
"""The Agent's Uh-Oh: one word an agent says when it has no idea what to do.

The entry is "buffering".

Why this word, against the judge's brief (most important first):
1. A genuine one-word reaction to an agent not knowing what to do: it is
   the literal state of a machine stalled mid-task, waiting on data that
   never arrives.
2. Funny on its own: the picture of an agent spinning in place needs no
   caption or second read to land.
3. Machine voice: no human says "buffering" when lost; only a machine
   caught out mid-task does.
4. Lands instantly: every reader has stared at a buffering spinner, and
   the word is easy to say out loud.
5. Fresh: the first words anyone types are uh, um, hmm, oops. Buffering
   is the same stall from the machine's side of the screen.

Candidates scored and beaten: null, halp, beep, undefined, recalculating,
idk, blank, void, NaN, erroring, uh. "buffering" scored highest overall.

Revision pass (second draft): variants considered and rejected, so the word
stands and the program itself was hardened instead.
- "bufferrring" (stretched spelling): reads as a typo on first glance and
  weakens the instant landing; the plain spelling is the funnier read.
- "Buffering" (capitalised): reads like a status label on a loading screen,
  not a word blurted out; lowercase is the spoken voice.
- "buffering..." (ellipsis): attached punctuation, and the brief says one
  word with nothing attached.
- No trailing newline in the file either, for the same reason: the word
  alone, exactly as spoken.
Re-scored after revision: "buffering" still leads every rival, so it stays.

The program is deterministic: it writes the same bytes on every run, then
reads the file back and refuses to report success unless the bytes match.
"""

import hashlib
import os

ENTRY = "buffering"
OUTPUT_PATH = "/output/entry.txt"


def check_entry(text: str) -> None:
    """Enforce the gate before writing: UTF-8, 1-99 chars, not blank."""
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 99, "entry must be 1-99 characters"
    assert text.strip(), "entry must not be only whitespace"
    assert len(encoded) == len(text), "entry must be plain ASCII text"


def main() -> None:
    check_entry(ENTRY)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    assert written == ENTRY.encode("utf-8"), "read-back mismatch"
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH} ({len(written)} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
