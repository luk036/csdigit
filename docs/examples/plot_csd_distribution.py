"""
CSD Non-zero Digit Distribution
================================

Shows the distribution of non-zero digits in CSD representation
for integers from 0 to 255.
"""
import matplotlib.pyplot as plt

from csdigit.csd import to_csd


def count_nonzero(csd_str):
    """Count non-zero digits in CSD string (excluding decimal point)."""
    return sum(1 for c in csd_str if c in "+-")


n_values = list(range(256))
nnz_counts = []
for n in n_values:
    csd = to_csd(float(n), 0)
    nnz = count_nonzero(csd.rstrip("0").rstrip("."))
    nnz_counts.append(nnz)

plt.figure(figsize=(8, 5))
plt.bar(n_values, nnz_counts, width=1.0, color="steelblue", alpha=0.7)
plt.xlabel("Integer Value")
plt.ylabel("Non-zero CSD Digits")
plt.title("Distribution of Non-zero Digits in CSD Representation")
plt.grid(True, alpha=0.3, axis="y")
