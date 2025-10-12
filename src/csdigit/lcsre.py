"""
Longest Repeated Substring Finder

This code defines a function called longest_repeated_substring that finds the longest repeated
non-overlapping substring within a given string. The purpose of this code is to identify and return the
longest sequence of characters that appears more than once in the input string, without the repetitions
overlapping each other.

The function takes a single input: a string called cs, which represents the text in which we want to

find the repeated substring. The output of the function is another string, which is the longest repeated

non-overlapping substring found in the input.

To achieve its purpose, the code uses a dynamic programming approach. It creates a 2D table (called LCSRe) to keep track of the lengths of repeated substrings at different positions in the input string. The algorithm then iterates through this table, comparing characters and updating the lengths of repeated substrings it finds.

The main logic flow of the algorithm is as follows:

1. Initialize the 2D table with zeros.
2. Iterate through the table, comparing characters of the input string.
3. When matching characters are found, update the length of the repeated substring in the table.
4. Keep track of the maximum length of repeated substring found and its ending position.
5. After filling the table, extract the longest repeated substring from the input string using the recorded length and position.

An important aspect of this algorithm is that it avoids overlapping substrings. This is achieved by checking if the distance between the current positions is greater than the length of the previously found repeated substring.

The code also includes a simple example usage, where it applies the function to the string "+-00+-00+-00+-0". This demonstrates how the function can be used and what kind of output it produces.

In summary, this code provides a way to find the longest sequence of characters that repeats in a given
text, which can be useful in various text processing and analysis tasks. It uses a clever approach to
solve what could otherwise be a computationally expensive problem, making it efficient for longer input
strings.
"""

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
