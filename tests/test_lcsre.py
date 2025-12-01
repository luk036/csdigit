from csdigit.lcsre import longest_repeated_substring


def test_lcsre() -> None:
    assert longest_repeated_substring("+-00+-00+-00+-0") == "+-00+-0"
    assert longest_repeated_substring("abcdefgh") == ""


def test_longest_repeated_substring() -> None:
    # Test case 1:
    cs = "+-00+-00+-00+-0"
    expected = "+-00+-0"
    assert longest_repeated_substring(cs) == expected

    # Test case 2:
    cs = "banana"
    expected = "an"
    assert longest_repeated_substring(cs) == expected

    # Test case 3:
    cs = "abcdefghijklmnopqrstuvwxyz"
    expected = ""
    assert longest_repeated_substring(cs) == expected
