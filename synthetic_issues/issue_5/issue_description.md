# PathCollection.legend_elements fails with masked arrays and edge cases

## Description
I've encountered several issues with the `PathCollection.legend_elements()` method, which is commonly used to create legends for scatter plots. The method fails in various edge cases:

1. When using masked arrays for colors, the method raises an error because it doesn't properly handle the mask.

2. When all data points have the same value, the legend creation fails because the interpolation logic doesn't handle this case correctly.

3. When using negative values for sizes, the method either fails or produces incorrect results.

4. When using a non-monotonic function for the `func` parameter, the interpolation can produce incorrect results.

5. When working with empty collections or collections with empty paths, the method raises cryptic errors instead of gracefully returning empty legend elements.

These issues make it difficult to use the legend_elements method in real-world scenarios where data might have these characteristics.

## Steps to Reproduce
1. Create a scatter plot with masked array values:
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.arange(10)
y = np.arange(10)
c = np.ma.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], mask=[0, 0, 1, 0, 0, 1, 0, 0, 0, 0])

fig, ax = plt.subplots()
scatter = ax.scatter(x, y, c=c, cmap='viridis')
handles, labels = scatter.legend_elements()  # This raises an error
ax.legend(handles, labels)
plt.show()
```

2. Create a scatter plot with all points having the same value:
```python
c = np.ones(10) * 5  # All values are 5
scatter = ax.scatter(x, y, c=c, cmap='viridis')
handles, labels = scatter.legend_elements()  # This raises an error
```

3. Create a scatter plot with negative sizes:
```python
s = np.array([-10, 0, 10, 20, 30, 40, 50, 60, 70, 80])
scatter = ax.scatter(x, y, s=s)
handles, labels = scatter.legend_elements(prop="sizes")  # This produces incorrect results
```

## Expected Behavior
1. Masked arrays should be handled correctly, with legend elements created only for unmasked values.
2. When all data points have the same value, a single legend element should be created.
3. Negative sizes should be handled gracefully, either by filtering them out or by using their absolute values.
4. Non-monotonic functions should be handled correctly, possibly by sorting the values before interpolation.
5. Empty collections should return empty legend elements without raising errors.

## Actual Behavior
1. With masked arrays, the method raises an error because it tries to use `np.unique` on a masked array without properly handling the mask.
2. With single-value arrays, the interpolation fails because min equals max.
3. With negative sizes, the method either raises errors or produces incorrect legend elements.
4. With non-monotonic functions, the interpolation can produce incorrect or unexpected results.
5. With empty collections, the method raises index errors when trying to access empty arrays.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: macOS 12.6

## Additional Context
This issue affects data exploration workflows where legends are important for understanding the data, especially when working with real-world datasets that may contain masked values, outliers, or other edge cases.