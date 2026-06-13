"""
Longest Repeated Non-Overlapping Substring (LCSRe) finder.

Finds the longest substring that appears at least twice in the input string
without overlapping occurrences. Uses dynamic programming with a space-optimized
2-row DP table (O(n) memory instead of O(n\\u00b2)).

This is used internally by the CSD multiplier generator to detect repeated
patterns in CSD strings, enabling hardware sharing via sub-expression wires.

Reference:
    https://www.geeksforgeeks.org/longest-repeating-and-non-overlapping-substring/
"""

# Python 3 program to find the longest repeated
# non-overlapping substring


def longest_repeated_substring(csd_string: str) -> str:
    """Longest repeated non-overlapping substring

    The `longest_repeated_substring` function takes a string as input and returns the longest repeated
    substring in the string.

    :param csd_string: The parameter `csd_string` is a string containing the CSD value

    :type csd_string: str

    :return: The function `longest_repeated_substring` returns a string, which is the longest repeated
        substring in the given input string `csd_string`.

    Examples:
        >>> longest_repeated_substring("+-00+-00+-00+-0")
        '+-00+-0'
    """
    num_dimensions = len(csd_string) + 1
    # Flat 2-row DP table: avoids O(n²) memory and double-list indirection
    LCSRe = [0] * (2 * num_dimensions)

    result = ""  # To store result
    result_length = 0  # To store length of result

    # building table in bottom-up manner
    index = 0
    for row_index in range(1, num_dimensions):
        cur_row = (row_index % 2) * num_dimensions
        prev_row = ((row_index - 1) % 2) * num_dimensions
        for col_index in range(row_index + 1, num_dimensions):
            # (col_index-row_index) > LCSRe[row_index-1][col_index-1] to remove
            # overlapping
            if csd_string[row_index - 1] == csd_string[col_index - 1] and LCSRe[
                prev_row + col_index - 1
            ] < (col_index - row_index):
                LCSRe[cur_row + col_index] = LCSRe[prev_row + col_index - 1] + 1

                # updating maximum length of the
                # substring and updating the finishing
                # index of the suffix
                if LCSRe[cur_row + col_index] > result_length:
                    result_length = LCSRe[cur_row + col_index]
                    index = max(row_index, index)

            else:
                LCSRe[cur_row + col_index] = 0

    # If we have non-empty result, then insert
    # all characters from first character to
    # last character of string
    if result_length > 0:
        # for row_index in range(index - result_length + 1, index + 1):
        #     result = result + csd_string[row_index - 1]
        result = csd_string[index - result_length : index]

    return result


# Driver Code
if __name__ == "__main__":
    csd_string = "+-00+-00+-00+-0"
    print(longest_repeated_substring(csd_string))

# This code is contributed by ita_c
