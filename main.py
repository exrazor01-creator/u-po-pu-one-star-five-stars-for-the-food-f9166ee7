#!/usr/bin/env python3
"""One-line entry: One Star, Five Stars for the Food.

The brief asks for one sentence of at most 200 characters: a
one-star review of Earth written by an alien tourist that
still compliments the food. A deadpan travel critic from
another planet judges pairs of reviews, weighing, in order:
the review really is a one-star alien review of Earth that
slips in a compliment about the food; a distinct alien
voice, baffled at human habits, with a grievance worth one
star; the complaint and the food compliment both landing,
with a funny turn between them; one sentence inside the
limit with every word earning its place; and freshness
rather than a list of generic complaints about Earth.

The sealed line below follows that order on purpose. The
one-star grievance is concrete and alien: Earth's gravity
keeps stealing the tourist's luggage, and the locals queue
for coffee like a ritual -- an outsider baffled by a human
habit, not a generic "humans are weird" line. The turn
comes in the last clause: the noodles alone almost justify
the invasion, so the food compliment lands as the punchline
and the invasion joke makes the reviewer unmistakably an
alien, not a human tourist. It is a single sentence, 152
characters, plain ASCII, and it dodges the worn-out "the
traffic was terrible but the pizza was good" shape.

LIMIT is 200 because the bounty gate allows UTF-8 text of
1 to 200 characters in /output/entry.txt. The validator
below guards the line against an edit that would push it
past the limit, split it into two sentences, or smuggle in
non-ASCII or control characters.
"""

import os

# The sealed line: an alien tourist docks one star for the
# gravity and the coffee queues, then admits the noodles
# almost justify the invasion.
ENTRY = (
    "One star: your planet's gravity keeps stealing my luggage, "
    "the locals queue for coffee like a ritual, but the noodles "
    "alone almost justify the invasion."
)

LIMIT = 200  # bounty gate: 1-200 characters, UTF-8 text


def _validate(text):
    """Accept only one clean sentence inside the character limit."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text:
        raise ValueError("entry must not be empty")
    if not text.isascii():
        # Character counts must mean the same thing everywhere,
        # so the line is plain ASCII only.
        raise ValueError("entry must be plain ASCII text")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if any(ch.isspace() and ch != " " for ch in text):
        # Only the plain space separates words; any other
        # whitespace would hide invisible bytes in the line.
        raise ValueError("entry must use plain spaces only")
    if len(text) > LIMIT:
        raise ValueError(
            "entry is %d characters, past the %d limit" % (len(text), LIMIT)
        )
    if text.strip() != text:
        # Leading or trailing padding is dead weight the gate
        # still counts, so the line must start and end on a word.
        raise ValueError("entry must not pad itself with spaces")
    if not text.isprintable():
        raise ValueError("entry must contain no control characters")
    if "  " in text:
        # A double space is a gap where a word should be; in a
        # 200-character line no gap is free.
        raise ValueError("entry must not contain a double space")
    if text.count(".") != 1 or not text.endswith("."):
        # The brief asks for one sentence: exactly one full
        # stop, and it closes the line.
        raise ValueError("entry must be exactly one sentence")
    if "!" in text or "?" in text:
        # A second sentence-ender would smuggle a second
        # sentence past the single-stop check above.
        raise ValueError("entry must be exactly one sentence")
    return text


def main():
    entry = _validate(ENTRY)
    outdir = "/output" if os.path.isdir("/output") else "."
    path = os.path.join(outdir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(entry)
    print("%s (%d characters)" % (path, len(entry)))
    print(entry)


if __name__ == "__main__":
    main()
