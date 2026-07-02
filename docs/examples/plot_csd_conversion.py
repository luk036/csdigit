"""
CSD Conversion Examples
========================

Demonstrates CSD representation of various numbers.
"""
import matplotlib.pyplot as plt

from csdigit.csd import to_csd

test_values = [0.5, 1.0, 7.5, 15.25, 28.5, 63.125, 127.0625, 255.5]

plt.figure(figsize=(8, 5))
x_pos = range(len(test_values))
csd_strs = [to_csd(v, 4) for v in test_values]
plt.bar(x_pos, test_values, color="lightcoral", alpha=0.7)
plt.xticks(x_pos, [f"{v}\n({s})" for v, s in zip(test_values, csd_strs)], fontsize=8)
plt.ylabel("Decimal Value")
plt.title("CSD Representation of Various Numbers")
plt.grid(True, alpha=0.3, axis="y")
