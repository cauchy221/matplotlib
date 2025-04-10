# TwoSlopeNorm produces incorrect colors with extreme value ranges

## Description
I've discovered a bug in the `TwoSlopeNorm` class that causes incorrect color mapping when there's a significant difference in scale between the negative and positive ranges. This is particularly problematic when visualizing data with very different scales on either side of the center value.

For example, when visualizing data that ranges from -0.01 to 100 with a center at 0, the colors in the negative range are compressed into a tiny portion of the colormap, while the positive range is stretched. This makes it impossible to see variations in the negative range.

The issue appears to be in the normalization calculation in the `__call__` method, which doesn't properly handle extreme differences in scale between the ranges.

Additionally, there seems to be a discontinuity at the center point, where values exactly equal to `vcenter` are handled differently than values slightly above or below it.

## Steps to Reproduce
1. Create a dataset with very different scales on either side of zero:
```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# Create data with extreme ranges
x = np.linspace(-1, 1, 100)
y = np.linspace(-1, 1, 100)
X, Y = np.meshgrid(x, y)
Z = np.zeros_like(X)
Z[X+Y < 0] = (X+Y)[X+Y < 0] * 0.01  # Small negative range
Z[X+Y >= 0] = (X+Y)[X+Y >= 0] * 100  # Large positive range

# Plot with TwoSlopeNorm
plt.figure()
plt.pcolormesh(X, Y, Z, cmap='coolwarm',
               norm=mcolors.TwoSlopeNorm(vcenter=0, vmin=-0.02, vmax=200))
plt.colorbar()
plt.title('Buggy TwoSlopeNorm Behavior')
plt.show()
```

2. Observe that the negative values (which should be blue) are all compressed into a single shade of blue, making it impossible to distinguish between different negative values.

## Expected Behavior
The normalization should properly distribute colors across both ranges, regardless of their relative scales. The negative range should use the full blue spectrum of the colormap, and the positive range should use the full red spectrum.

Values exactly at the center point should be handled consistently with the interpolation used for other values.

## Actual Behavior
1. When there's a large difference in scale between negative and positive ranges, one side of the colormap is severely compressed.
2. Values exactly equal to `vcenter` may be handled inconsistently compared to values slightly above or below it.
3. The normalization doesn't properly distribute colors across the full range of the colormap when scales are very different.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue is particularly important for scientific visualization where data often has very different scales on either side of a meaningful center point (like zero). The current implementation makes it difficult to visualize such data effectively.