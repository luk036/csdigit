import random


def generate_string(length):
    # Choose a random character from '+', '0', '-'
    characters = "+0-"
    result = ""
    for _ in range(length):
        result += random.choice(characters)
    return result


def generate_list(n, length):
    result = []
    for _ in range(n):
        result.append(generate_string(length))
    return result


# Generate a list of 10 strings, each of length 8
lst = generate_list(10, 9)
for i in range(10):
    print(lst[i])
