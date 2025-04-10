# Colormap visualization breaks when data range is very small

## Description
I'm trying to visualize data with a very small range (e.g., values between 0.1 and 0.11), but the colormap doesn't show a proper gradient. Instead, it seems to only use two colors (the min and max of the colormap), creating a binary/step visualization instead of a smooth gradient.

## Steps to Reproduce
1. Create a dataset with a very small range (e.g., values between 0.1 and 0.11)
2. Create a plot with a colormap using this data
3. Observe that instead of a smooth gradient, the visualization shows only two colors

```python
import numpy as np
import matplotlib.pyplot as plt

# Create data with small range
x = np.linspace(0, 10, 100)
y = np.linspace(0, 10, 100)
X, Y = np.meshgrid(x, y)
Z = 0.1 + 0.01 * np.sin(X) * np.cos(Y)  # Values between 0.1 and 0.11

# Plot with colormap
plt.figure(figsize=(8, 6))
plt.pcolormesh(X, Y, Z, cmap='viridis')
plt.colorbar()
plt.title('Data with small range (0.1 to 0.11)')
plt.show()
```

## Expected Behavior
The colormap should show a smooth gradient from the minimum to maximum color in the colormap, properly representing the data range.

## Actual Behavior
The colormap only shows two colors (the min and max of the colormap), creating a binary/step visualization instead of a smooth gradient. This makes it impossible to see the subtle variations in my data.

## Environment
- Matplotlib version: 3.7.1
- Python version: 3.10.4
- Operating System: Ubuntu 22.04

## Additional Information
This issue only occurs when the data range is very small (approximately < 1e-5). When I artificially increase the range of my data (e.g., by multiplying by 1000), the colormap works as expected.

I've attached a screenshot showing the binary/step visualization I'm getting versus what I would expect to see.