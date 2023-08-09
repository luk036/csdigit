from csdigit.lcsre import longest_repeated_substring


def test_lcsre():
    assert longest_repeated_substring("+-00+-00+-00+-0") == "+-00+-0"
    assert longest_repeated_substring("abcdefgh") == ""
