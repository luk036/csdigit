# Python 3 program to find the longest repeated
# non-overlapping substring


def longest_repeated_substring(cs: str) -> str:
    """Longest repeated non-overlapping substring

    The `longest_repeated_substring` function takes a string as input and returns the longest repeated
    substring in the string.

    :param cs: The parameter `cs` is a string containing the CSD value

    :type cs: str

    :return: The function `longest_repeated_substring` returns a string, which is the longest repeated
        substring in the given input string `cs`.

    Examples:
        >>> longest_repeated_substring("+-00+-00+-00+-0")
        '+-00+-0'
    """
    ndim = len(cs) + 1
    LCSRe = [[0 for _ in range(ndim)] for _ in range(ndim)]

    res = ""  # To store result
    res_length = 0  # To store length of result

    # building table in bottom-up manner
    index = 0
    for i in range(1, ndim):
        for j in range(i + 1, ndim):
            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if cs[i - 1] == cs[j - 1] and LCSRe[i - 1][j - 1] < (j - i):
                LCSRe[i][j] = LCSRe[i - 1][j - 1] + 1

                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if LCSRe[i][j] > res_length:
                    res_length = LCSRe[i][j]
                    index = max(i, index)

            else:
                LCSRe[i][j] = 0

    # If we have non-empty result, then insert
    # all characters from first character to
    # last character of string
    if res_length > 0:
        # for i in range(index - res_length + 1, index + 1):
        #     res = res + cs[i - 1]
        res = cs[index - res_length : index]

    return res


# Driver Code
if __name__ == "__main__":
    cs = "+-00+-00+-00+-0"
    print(longest_repeated_substring(cs))

# This code is contributed by ita_c
