from csdigit.csd import (
    to_csd,
    to_csd_i,
    to_csdnnz,
    to_csdnnz_i,
    to_decimal,
    to_decimal_using_pow,
)

print("=== to_csd (float) ===")
for v, p in [
    (28.5, 2),
    (-0.5, 2),
    (0.0, 2),
    (2.5, 4),
    (0.0, 0),
    (7.0, 0),
    (-7.0, 0),
    (28.5, 0),
]:
    res = to_csd(v, p)
    print(f'  to_csd({v}, {p}) = "{res}"')

print()
print("=== to_csd_i (integer) ===")
for v in [28, 0, -28, 7, -7, 1, -1]:
    res = to_csd_i(v)
    print(f'  to_csd_i({v}) = "{res}"')

print()
print("=== to_decimal ===")
for s in ["+00-00.+", "0.-", "0", "0.0", "0.+", "0.-", "0.++", "0.-+", "+00-00"]:
    res = to_decimal(s)
    print(f'  to_decimal("{s}") = {res}')

print()
print("=== to_decimal_using_pow (integer CSD) ===")
for s in ["+00-00", "0", "-00+00"]:
    res = to_decimal_using_pow(s)
    print(f'  to_decimal_using_pow("{s}") = {res}')

print()
print("=== to_csdnnz (float, limited nnz) ===")
for v, n in [(28.5, 4), (-0.5, 4), (0.0, 4), (0.5, 4), (0.0, 0), (28.5, 2), (28.5, 1)]:
    res = to_csdnnz(v, n)
    print(f'  to_csdnnz({v}, {n}) = "{res}"')

print()
print("=== to_csdnnz_i (integer, limited nnz) ===")
for v, n in [(28, 4), (0, 4)]:
    res = to_csdnnz_i(v, n)
    print(f'  to_csdnnz_i({v}, {n}) = "{res}"')
