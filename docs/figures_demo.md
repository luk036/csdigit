# Figures Demo

Auto-generated figures demonstrating csdigit functionality.

## CSD Non-zero Digit Distribution

```{plot} examples/plot_csd_distribution.py
```

## CSD Conversion Examples

```{plot} examples/plot_csd_conversion.py
```

### Inline Plot Example

```{plot}
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
plt.plot(x, np.sin(x))
plt.title("Simple Sine Wave")
plt.grid(True, alpha=0.3)
```
