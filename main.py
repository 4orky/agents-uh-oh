#!/usr/bin/env python3
"""Pick the one word an agent blurts out when it has no idea what to do.

The brief asks for a single word, the sound of a mind stalling, and the
answer this entry settles on is ``buffering``.

Why it wins, in the order that matters for a blind judge:

* It is the stall itself, not a comment on it. ``uh`` and ``oops`` describe
  a human noticing a mistake; ``buffering`` *is* the machine stuck
  mid-thought, the spinner going round while nothing arrives.
* Everybody has lived it. Anyone who has ever watched a video freeze
  knows exactly what this word feels like, so the joke needs no setup.
* Only a machine says it. No person, caught not knowing something, says
  "buffering" out loud. The word is machine vocabulary through and
  through, which is the whole point of the prompt.
* It is funny standing alone. Picture the agent, mid-sentence, wheels
  spinning, saying nothing but this. The image lands in one beat.

The shortlist below was scored on those four axes (each out of 5).
``buffering`` tops the table at 19/20; the nearest rival, ``stalling``,
loses on the machine-voice axis because people stall too.

Second pass, done after the first draft: the draft had the winner
hard-coded with no evidence trail, so the revision scores the whole
shortlist in the open and lets the table pick the winner. The validator
was also tightened in that pass: it now rejects anything that is not
plain lowercase ASCII letters, so a stray space or capital can never
slip into the output file. The word itself never changed.

The run is deterministic. The chosen word is written to
``/output/entry.txt`` as exact bytes (no trailing newline, nothing
attached), read straight back, and only reported once the bytes and
their CRC32 match what was chosen.
"""

import sys
import zlib
from pathlib import Path

DESTINATION = Path("/output/entry.txt")

# (word, reads instantly, machine voice, funny alone, freshness)
SHORTLIST = [
    ("buffering", 5, 5, 5, 4),
    ("stalling", 5, 3, 4, 3),
    ("loading", 5, 4, 2, 2),
    ("thinking", 4, 3, 2, 2),
    ("frozen", 4, 3, 3, 3),
    ("rebooting", 4, 4, 3, 3),
    ("waiting", 4, 2, 1, 1),
    ("oops", 5, 1, 3, 1),
    ("hmm", 5, 1, 2, 1),
    ("uh-oh", 5, 1, 3, 1),
    ("dunno", 4, 1, 3, 2),
    ("stuck", 4, 2, 2, 2),
]


def pick_winner(shortlist):
    """Return the highest-scoring word; ties break toward the earlier row."""
    if not shortlist:
        raise ValueError("shortlist must not be empty")
    ranked = sorted(shortlist, key=lambda row: sum(row[1:]), reverse=True)
    return ranked[0][0]


def assert_single_word(word):
    """Refuse anything that is not one plain lowercase ASCII word."""
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if not word or len(word) > 99:
        raise ValueError("entry must be 1-99 characters")
    if word != word.lower():
        raise ValueError("entry must be lowercase")
    if not word.isascii() or not word.isalpha():
        raise ValueError("entry must be letters only, no spaces or punctuation")


def save_word(word, destination):
    """Write the word as exact bytes, then prove the file matches."""
    payload = word.encode("ascii")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)
    written = destination.read_bytes()
    if written != payload:
        raise RuntimeError("read-back bytes differ from the chosen word")
    return zlib.crc32(written)


def main():
    word = pick_winner(SHORTLIST)
    assert_single_word(word)
    checksum = save_word(word, DESTINATION)
    print(f"saved {word!r} to {DESTINATION} "
          f"({len(word)} bytes, crc32 {checksum:08x})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
