from pytest_cases import fixture, parametrize_with_cases

from disquip.grep import grep


@fixture
def multiline_simple():
    return """
hello there
this is a big string
that we'll be using for testing
Here Is a Line With Mixed Case
HELLO, friend.
GOODbye moonman
this is a line that contains the word this and there
    """


def case_hello(multiline_simple):
    return multiline_simple.splitlines(), "hello", ["hello there", "HELLO, friend."]


def case_is(multiline_simple):
    return multiline_simple.splitlines(), "is", ["this is a big string", "Here Is a Line With Mixed Case", "this is a line that contains the word this and there"]


@parametrize_with_cases("txt,pat,expected", cases=".")
def test_grep(txt, pat, expected):
    actual = grep(txt, pat)
    assert actual == expected

