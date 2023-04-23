# Python 3 program to find the longest repeated
# non-overlapping substring

# Returns the longest repeating non-overlapping
# substring in csd_str
def longest_repeated_substring(csd_str: str) -> str:
    n = len(csd_str)
    LCSRe = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

    res = ""  # To store result
    res_length = 0  # To store length of result

    # building table in bottom-up manner
    index = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):

            # (j-i) > LCSRe[i-1][j-1] to remove
            # overlapping
            if csd_str[i - 1] == csd_str[j - 1] and \
                    LCSRe[i - 1][j - 1] < (j - i):
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
        for i in range(index - res_length + 1, index + 1):
            res = res + csd_str[i - 1]

    return res


# Driver Code
if __name__ == "__main__":
    csd_str = "+-00+-00+-00+-0"
    print(longest_repeated_substring(csd_str))

# This code is contributed by ita_c
