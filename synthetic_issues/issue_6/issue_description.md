# Figure.legend() replaces existing legends and has issues with empty axes

## Description
I've discovered several issues with the `Figure.legend()` method:

1. When calling `fig.legend()` multiple times, each new legend replaces all existing legends instead of adding a new one. This makes it impossible to have multiple legends in different positions on the same figure.

2. When calling `fig.legend()` on a figure with no axes, it raises an error instead of gracefully creating an empty legend.

3. When a legend is created and later removed, subsequent attempts to interact with the figure can cause errors because the legend removal process is incomplete.

4. When custom transforms are provided in the `bbox_transform` parameter, they are ignored and overwritten with the default transform.

5. Non-string labels are not properly handled, which can cause errors when trying to display the legend.

These issues make it difficult to create complex figures with multiple legends or to programmatically create legends in a robust way.

## Steps to Reproduce
1. Create multiple legends on the same figure:
```python
import matplotlib.pyplot as plt

fig, (ax1, ax2) = plt.subplots(1, 2)
line1 = ax1.plot([1, 2, 3], label="Line 1")[0]
line2 = ax2.plot([3, 2, 1], label="Line 2")[0]

# Create first legend
leg1 = fig.legend(handles=[line1], loc="upper left")

# Create second legend - this should add a new legend, not replace the existing one
leg2 = fig.legend(handles=[line2], loc="upper right")

# Only the second legend is visible
plt.show()
```

2. Create a legend on a figure with no axes:
```python
fig = plt.figure()
leg = fig.legend()  # This raises an error
plt.show()
```

3. Remove a legend and then interact with the figure:
```python
fig, ax = plt.subplots()
line = ax.plot([1, 2, 3], label="Line")[0]
leg = fig.legend()
leg.remove()
# Further operations on the figure may cause errors
```

## Expected Behavior
1. Each call to `fig.legend()` should create a new legend and add it to the figure, not replace existing legends.
2. Calling `fig.legend()` on a figure with no axes should create an empty legend without errors.
3. Legend removal should completely clean up all references to prevent errors.
4. Custom transforms provided in `bbox_transform` should be respected and not overwritten.
5. Non-string labels should be properly converted to strings.

## Actual Behavior
1. Each call to `fig.legend()` replaces all existing legends, so only the last legend created is visible.
2. Calling `fig.legend()` on a figure with no axes raises an error.
3. After removing a legend, some references remain, which can cause errors.
4. Custom transforms are ignored and overwritten with the default transform.
5. Non-string labels can cause errors when displaying the legend.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: macOS 12.6

## Additional Context
This issue is particularly important for creating complex figures with multiple legends, which is a common need in scientific visualization. The current behavior makes it difficult to create such figures programmatically.