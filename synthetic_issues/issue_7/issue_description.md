# Contour plots fail or produce incorrect results with certain data ranges and level specifications

## Description
I've encountered several issues with contour plots in matplotlib when working with certain types of data and level specifications:

1. When plotting data with a very small range (e.g., values that differ by only 1e-10), the contour levels can become invalid or contain NaN values, causing the plot to fail or display incorrectly.

2. When specifying duplicate contour levels (e.g., `[1, 1, 2, 3]`), instead of raising an error as expected, the contour function sometimes silently modifies the levels, resulting in unexpected plots.

3. When specifying non-increasing contour levels (e.g., `[1, 2, 1.5, 3]`), the function sometimes sorts the levels instead of raising an error, which can lead to confusion when the order of levels is important.

4. When creating filled contours with a single level, the function sometimes creates a plot with two artificial levels instead of raising an error.

5. When plotting constant data (all values the same), the contour function sometimes produces invalid levels or crashes.

These issues make it difficult to create reliable contour plots, especially when working with scientific data that may have small variations or when precise control over contour levels is required.

## Steps to Reproduce
1. Create a contour plot with data having a very small range:
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
X, Y = np.meshgrid(x, y)
Z = np.ones_like(X) + 1e-10 * X  # Very small variation

fig, ax = plt.subplots()
cs = ax.contour(X, Y, Z, 5)  # This produces invalid levels
plt.show()
```

2. Create a contour plot with duplicate levels:
```python
Z = X + Y
cs = ax.contour(X, Y, Z, [1, 1, 1, 2, 3])  # This should raise an error but doesn't
```

3. Create a contour plot with non-increasing levels:
```python
cs = ax.contour(X, Y, Z, [1, 2, 1.5, 3])  # This should raise an error but sometimes doesn't
```

4. Create a filled contour plot with a single level:
```python
cs = ax.contourf(X, Y, Z, [1])  # This should raise an error but sometimes creates a plot
```

5. Create a contour plot with constant data:
```python
Z = np.ones_like(X)  # Constant data
cs = ax.contour(X, Y, Z, 5)  # This can produce invalid levels
```

## Expected Behavior
1. Contour plots with small data ranges should produce valid, evenly spaced levels.
2. Specifying duplicate contour levels should always raise a clear error.
3. Specifying non-increasing contour levels should always raise a clear error.
4. Creating filled contours with a single level should always raise a clear error.
5. Contour plots with constant data should either produce a single level or raise a clear error.

## Actual Behavior
1. Contour plots with small data ranges sometimes produce NaN levels or crash.
2. Duplicate contour levels are sometimes silently modified instead of raising an error.
3. Non-increasing contour levels are sometimes sorted instead of raising an error.
4. Filled contours with a single level sometimes create a plot with artificial levels.
5. Contour plots with constant data sometimes produce invalid levels or crash.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue is particularly important for scientific visualization where data may have small variations or where precise control over contour levels is required. The current behavior can lead to misleading visualizations or unexpected errors.