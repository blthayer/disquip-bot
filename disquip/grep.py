import re


def grep(txt: str, pat: str) -> list:
    """Pseudo-grep style line-by-line searching in the given string.
    Case insensitive.
    """
    # Don't worry about compiling the expressions. See the note here:
    # https://docs.python.org/3.6/library/re.html#re.compile

    hits = []
    for line in re.split("\n", txt):
        if re.search(pat, line, re.IGNORECASE):
            hits.append(line)

    return hits
