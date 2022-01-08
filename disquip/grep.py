import re


def grep(lines: list, pat: str) -> list:
    """Pseudo-grep style line-by-line searching in the given list of
    strings (assumed to be lines). Case insensitive.
    """
    # Don't worry about compiling the expressions. See the note here:
    # https://docs.python.org/3.6/library/re.html#re.compile
    hits = []
    for line in lines:
        if re.search(pat, line, re.IGNORECASE):
            hits.append(line)

    return hits
