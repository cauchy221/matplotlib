# Legend initialization fails with various input edge cases

## Description
I've encountered several issues with the `Legend` class in matplotlib when working with certain edge cases:

1. When creating a legend with empty handles and labels, the code crashes instead of handling this case gracefully.

2. When handles and labels have different lengths, the code silently truncates the longer list, which can lead to unexpected behavior.

3. When a label is `None` or not convertible to a string, the code crashes with a cryptic error message.

4. When `ncols` is set to 0 or a negative value, the code crashes with a division by zero error.

5. When `handleheight` is very small (< 0.7), the calculated descent becomes negative, which can lead to incorrect rendering.

6. When creating a legend for an axes without a figure, the code crashes with an attribute error.

7. When using an invalid alignment value, the code crashes with a cryptic error message.

These issues make it difficult to create reliable legends, especially in automated plotting scenarios where the inputs might be dynamically generated.

## Steps to Reproduce
1. Create a legend with empty handles and labels:
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
legend = ax.legend([], [])
fig.canvas.draw()  # This crashes
```

2. Create a legend with mismatched handles and labels:
```python
fig, ax = plt.subplots()
line = ax.plot([0, 1], [0, 1])[0]
legend = ax.legend([line], ["label1", "label2"])  # This silently truncates the labels
fig.canvas.draw()
```

3. Create a legend with None labels:
```python
fig, ax = plt.subplots()
line = ax.plot([0, 1], [0, 1])[0]
legend = ax.legend([line], [None])  # This crashes
fig.canvas.draw()
```

4. Create a legend with zero ncols:
```python
fig, ax = plt.subplots()
line = ax.plot([0, 1], [0, 1], label="line")[0]
legend = ax.legend(ncols=0)  # This crashes
fig.canvas.draw()
```

5. Create a legend with very small handleheight:
```python
fig, ax = plt.subplots()
line = ax.plot([0, 1], [0, 1], label="line")[0]
legend = ax.legend(handleheight=0.5)  # This can lead to incorrect rendering
fig.canvas.draw()
```

6. Create a legend for an axes without a figure:
```python
from matplotlib.figure import Figure
ax = plt.Axes(Figure(), [0, 0, 1, 1])
line = ax.plot([0, 1], [0, 1], label="line")[0]
legend = ax.legend()  # This crashes
legend.draw(ax.figure.canvas.get_renderer())
```

7. Create a legend with invalid alignment:
```python
fig, ax = plt.subplots()
line = ax.plot([0, 1], [0, 1], label="line")[0]
legend = ax.legend(alignment="invalid")  # This crashes
fig.canvas.draw()
```

## Expected Behavior
1. Legends with empty handles and labels should be handled gracefully, either by creating an empty legend or raising a clear error.
2. Legends with mismatched handles and labels should raise a clear error.
3. Legends with None or non-string labels should convert them to strings or raise a clear error.
4. Legends with invalid ncols should raise a clear error.
5. Legends with very small handleheight should handle the negative descent gracefully.
6. Legends for axes without a figure should raise a clear error.
7. Legends with invalid alignment should raise a clear error.

## Actual Behavior
1. Legends with empty handles and labels crash with a cryptic error.
2. Legends with mismatched handles and labels silently truncate the longer list.
3. Legends with None labels crash with a TypeError.
4. Legends with zero ncols crash with a division by zero error.
5. Legends with very small handleheight have incorrect rendering due to negative descent.
6. Legends for axes without a figure crash with an attribute error.
7. Legends with invalid alignment crash with a cryptic error.

## Environment
- Matplotlib version: 3.7.0
- Python version: 3.9.7
- Operating system: Ubuntu 20.04

## Additional Context
This issue is particularly important for automated plotting scenarios where the inputs might be dynamically generated. The current behavior can lead to unexpected crashes or incorrect rendering.

I've attached a test script that demonstrates the issues with various test cases.